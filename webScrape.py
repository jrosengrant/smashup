from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
import io
from fighters import smash_ultimate_fighters

# BS4 method
# url = "https://ultimateframedata.com/stats"
# page = urlopen(url)
# html = page.read().decode("utf-8")
# soup = BeautifulSoup(html, "html.parser")
# print(soup.find('table', id='airaccelerationtable'))
# # for child in soup.descendants:
# #   if child.name == 'table':
# #     print(child)

# pandas method
# url = 'https://ultimateframedata.com/stats' 
# dfs = pd.read_html(url)
# combined_df = pd.concat(dfs)
# combined_df.to_csv('ultimate_framedata_stats.csv', index=False)

# WEB SCRAPING

# Scrape html of page
url = 'https://ultimateframedata.com/stats'
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# Get all tables from page
tables = soup.find_all('div', class_='statstablecontainer')
# print(tables)

# INITIALIZE DFS VAR
dfs = []
roll_data = []

# For each table:
# 1. Create data frame from table
# 3. Scrub Data in the dataframe according to list below
# 4. Append data frame to list of data frames

for table in tables:
  # print(table)
  df = pd.read_html(io.StringIO(str(table)))[0]
  title = table.find('h2').get_text()
  print(title)
  # print('INITIAL DF: \n', df.head())

  # DATA SCRUBBING
  # List of data issues to check for and scrub for each table:

  # Remove rank column
  if 'Rank' in df.columns:
    df.drop('Rank', axis=1, inplace=True)
  # print('POST DROP RANK: \n', df.head())

  # Prepend the title of the table to the column names to make it easier to tell what it means
  df.rename(columns={col: title+'_'+col for col in df.columns if col != "Character" }, inplace=True)
  # print('POST TITLE PREPEND: ', df.head())

  # RENAMES
  # DK vs Donkey Kong
    # DK used only for hardland/softland
  df['Character'] = df['Character'].replace('DK', 'Donkey Kong')

  # ROB is misspelled for hardland softland
  df['Character'] = df['Character'].replace('R.O.B', 'R.O.B.')

  #Pac-Man
  df.Character = df.Character.replace(['PAC-MAN', 'Pac Man'], 'Pac-Man', regex=True)

  #Meta Knight
  df.Character = df.Character.replace('Metaknight', 'Meta Knight')

  #Rosalina & Luma
  df.Character = df.Character.replace(['Rosalina and Luma', '^Rosalina$'], 'Rosalina & Luma', regex=True)

  #Rosalina & Luma
  df.Character = df.Character.replace(['Mii Sword Fighter'], 'Mii Swordfighter', regex=True)

  # ECHO FIGHTERS (Marth/Lucina, Ryu/Ken, Roy/Chrom, Samus/DarkSamus, Simon/Richter) are combined in some tables
  # Split any value in the Character column by the slash character, and expand into a separate column
  # Stack the two columns into one column, reset the index, and rename to Character again
  df_split = df['Character'].str.split('/', expand=True).stack().reset_index(level=1, drop=True).rename('Character')

  # Rename the new index column back to 'Index' to prepare for join
  df_split.index = df_split.index.rename('Index')

  # Turn the new column of Character names into a data frame, and join it to a copy of the original df with the Character column dropped, on the Index column (how = left)
  # Reset the index again after joining
  df = df_split.to_frame().join(df.drop('Character', axis=1), how='left').reset_index(drop=True)
  # if title == 'Landing': 
  #   print('SPLIT JOIN',df_split_join)

  # MULTI-FIGHTERS
    # Note: according to the official smash website, PT is 3 chars and Pyra/Mythra is 2. 
      # https://www.smashbros.com/en_GB/fighter/index.html
    # Ice Climbers
      # Split into leader/follower for dash, consolidate and make the one that differs a special case or take the max
      # Popo/Nana get their own rows for air acceleration and walk speed
    # Rosalina & Luma is split 4 ways



  # Function mergeLikeRows
  # Merges rows which have split out multiple pieces of a single fighter, e.g. ice climbers into pairs or pokemon trainer into its three pokemon
  # Inputs:
  # df = data frame to scrub
  # searchFor = string or array of strings to search for
  # replaceWith = new character name to give to the merged row
  # cb = callback function to use to merge the values together
  # Outputs: 
  # scrubbed data frame
  def mergeLikeRows(df, searchFor, replaceWith, cb):
    bool_mask = df.Character.str.contains('|'.join(searchFor), regex=True)
    if bool_mask.any():
      rows_to_merge = df[bool_mask]
      # print(rows_to_merge)
      new_values = rows_to_merge.drop('Character', axis=1).apply(cb)
      new_row = pd.DataFrame(new_values).transpose()
      columns = [col for col in df.columns]
      new_row['Character'] = replaceWith
      new_row = new_row.reindex(columns=columns)
      df.loc[bool_mask, :] = new_row.values[0]
      df = df.drop_duplicates()
      # print(df.to_string())
    
    return df

  df = mergeLikeRows(df, ["Ice Climbers.+"], "Ice Climbers", max)
  df = mergeLikeRows(df, ["Popo", "Nana"], "Ice Climbers", max)
  

# CHECK FOR MISSING FIGHTERS
  # Some tables don't have the correct number of fighters, check for which are missing
  def checkMissingFighters(df):
    # List of all 89 fighters
    all_fighters = smash_ultimate_fighters

    # Get the unique values in the 'Character' column
    unique_characters = df.Character.unique()

    # Find the missing fighters
    missing_fighters = [fighter for fighter in all_fighters if fighter not in unique_characters]

    # Print the missing fighters
    if missing_fighters: 
      print("Missing fighters:", missing_fighters)
      print(df.to_string())

  checkMissingFighters(df)
  

  # Grab range for Olimar differs by which pikmin and how many are out

  if title == 'Forward Rolls' or title == 'Backward Rolls':
    roll_data.append(df)

  dfs.append(df)
  
roll_data_to_csv = pd.concat(roll_data).to_csv('roll_data.csv', index=False)
combined_df = pd.concat(dfs)
combined_df_to_csv = combined_df.to_csv('scrubbed framedata.csv', index=False)

#IDEAS
    #add a table for meta data from me, such as
    #franchise/series they are from
    #hero vs villain
    #zoners, brawlers, reflectors