from django.db import models

# Create your models here.
class te_contacto(models.Model):
    co_id = models.AutoField(primary_key=True)
    co_nombre = models.CharField(max_length=50, blank=True)
    co_apellido = models.CharField(max_length=50)
    co_telefono = models.CharField(max_length=30, blank=True)
    co_institucion = models.CharField(max_length=10)
    class Meta:
        db_table = 'te_contacto'

    def __unicode__(self):
        return '%d, %s, %s, %s, %s' % (self.co_id, self.co_nombre, self.co_apellido, self.co_telefono, self.co_institucion)

class te_detalle_inspeccion(models.Model):
    de_id = models.AutoField(primary_key=True)
    de_id_inspeccion = models.IntegerField()
    de_id_listas = models.IntegerField()
    de_id_tareas = models.IntegerField()
    de_tarea_nombre = models.CharField(max_length=250)
    de_tarea_descripcion = models.CharField(max_length=250)
    de_resultado = models.IntegerField()
    de_observacion = models.CharField(max_length=500, blank=True)
    de_fecha = models.DateField()
    class Meta:
        db_table = 'te_detalle_inspeccion'

    def __unicode__(self):
        return '%d, %d, %d, %d, %s, %s, %d, %s, %s' % (self.de_id, self.de_id_inspeccion, self.de_id_listas, self.de_id_tareas, self.de_tarea_nombre, self.de_tarea_descripcion, self.de_resultado, self.de_observacion, self.de_fecha)

class te_inspeccion(models.Model):
    in_id = models.AutoField(primary_key=True)
    in_id_contacto = models.IntegerField()
    in_nombre_usuario = models.CharField(max_length=30)
    in_fecha = models.DateField(null=True, blank=True)
    in_avance = models.IntegerField(null=True, blank=True)
    in_fecha_final = models.DateTimeField(null=True, blank=True)
    in_frecuencia = models.CharField(max_length=10)
    in_id_lista = models.IntegerField()
    class Meta:
        db_table = 'te_inspeccion'

    def __unicode__(self):
        return '%d, %d, %s, %s, %s, %d' % (self.co_id, self.co_nombre, self.co_apellido, self.co_telefono, self.co_institucion, self.in_id_lista)

class te_listas(models.Model):
    li_id = models.IntegerField(primary_key=True)
    li_orden = models.IntegerField()
    li_nombre = models.TextField()
    li_frecuencia = models.CharField(max_length=10)
    li_descripcion = models.CharField(max_length=300, blank=True)
    class Meta:
        db_table = 'te_listas'

    def __unicode__(self):
        return '%d, %d, %s, %s, %s' % (self.li_id, self.li_orden, self.li_nombre, self.li_frecuencia, self.li_descripcion)

class te_tareas(models.Model):
    ta_id = models.IntegerField(primary_key=True)
    ta_orden = models.IntegerField()
    ta_nombre = models.CharField(max_length=250)
    ta_descripcion = models.CharField(max_length=300, blank=True)
    ta_resultado_esperado = models.IntegerField()
    ta_id_listas = models.IntegerField()
    class Meta:
        db_table = 'te_tareas'

    def __unicode__(self):
        return '%d, %d, %s, %s, %d, %d' % (self.ta_id, self.ta_orden, self.ta_nombre, self.ta_descripcion, self.ta_resultado_esperado, self.ta_id_listas)

class te_usuarios(models.Model):
    us_id = models.IntegerField(primary_key=True)
    us_usuario = models.CharField(max_length=100)
    us_password = models.CharField(max_length=100)
    us_id_contacto = models.IntegerField()
    us_nombre = models.CharField(max_length=200)
    us_correo = models.CharField(max_length=100)
    class Meta:
        db_table = 'te_usuarios'

    def __unicode__(self):
        return '%d, %s, %s, %d, %s, %s' % (self.us_id, self.us_usuario, self.us_password, self.us_id_contacto, self.us_nombre, self.us_correo)


class te_turno(models.Model):
    tu_id = models.AutoField(primary_key=True)
    tu_fecha_turno = models.DateField(null=True, blank=True)
    tu_tipo = models.CharField(max_length=20)
    tu_dia = models.CharField(max_length=20)
    tu_id_usuario = models.IntegerField()
    tu_nombre_usuario = models.CharField(max_length=100)
    tu_avance = models.FloatField()
    class Meta:
        db_table = 'te_turno'

    def __unicode__(self):
        return '%d, %s, %s, %s, %d, %s, %d' % (self.tu_id, self.tu_fecha_turno, self.tu_tipo, self.tu_dia, self.tu_id_usuario, self.tu_nombre_usuario, self.tu_avance)