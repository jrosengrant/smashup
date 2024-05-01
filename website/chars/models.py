from django.db import models

class Character(models.Model):
  char_name = models.CharField("Character Name", max_length=20)
  weight = models.IntegerField("Weight")
  num_jumps = models.IntegerField("Number of Jumps")
  max_run_vel = models.DecimalField("Maximum Run Velocity", max_digits=5, decimal_places=3)
  jump_height = models.DecimalField("Jump Height", max_digits=5, decimal_places=2)
  hop_height = models.DecimalField("Shorthop Height", max_digits=5, decimal_places=2)
  air_jump_height = models.DecimalField("Air Jump Height", max_digits=5, decimal_places=2)
  max_h_air_speed = models.DecimalField("Maximum Horizontal Air Speed", max_digits=5, decimal_places=3)
  fastfall_speed = models.DecimalField("Fastfall Speed", max_digits=5, decimal_places=3)
  has_walljump = models.BooleanField("Has Walljump")
  franchise = models.CharField(max_length=50)
  backstory = models.CharField(max_length=250)
  codename = models.CharField("Codename", max_length=20)
  img_url = models.CharField("Image File URL", max_length=50)

  def __str__(self):
    return self.char_name

