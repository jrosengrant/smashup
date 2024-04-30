from django.db import models

class Character(models.Model):
  char_name = models.CharField("character name", max_length=20)
  weight = models.IntegerField("weight")
  num_jumps = models.IntegerField("number of jumps")
  max_run_vel = models.DecimalField("maximum run velocity", max_digits=5, decimal_places=3)
  jump_height = models.DecimalField("jump height", max_digits=5, decimal_places=2)
  hop_height = models.DecimalField("shorthop height", max_digits=5, decimal_places=2)
  air_jump_height = models.DecimalField("air jump height", max_digits=5, decimal_places=2)
  max_h_air_speed = models.DecimalField("maximum horizontal air speed", max_digits=5, decimal_places=3)
  fastfall_speed = models.DecimalField("fastfall speed", max_digits=5, decimal_places=3)
  has_walljump = models.BooleanField("has walljump")
  franchise = models.CharField(max_length=50)
  backstory = models.CharField(max_length=250)

  def __str__(self):
    return self.char_name

