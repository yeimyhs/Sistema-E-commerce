# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remov` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import MinValueValidator

from django.core.exceptions import ValidationError
from django.conf import settings

from django.contrib.auth.models import AbstractUser, BaseUserManager



class Cupon(models.Model):
    idcupon = models.BigAutoField(db_column='idCupon', primary_key=True)  # Field name made lowercase.
    cantidaddescuento = models.FloatField()
    descripcion = models.TextField(blank=True, null=True)
    fechavigencia = models.DateTimeField(blank=True, null=True)
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Cupon'

#------------------------------------------------------------------
class Marca(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    imgen = models.ImageField(upload_to='marca/', blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'Marca'


class Moneda(models.Model):
    idmoneda = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Moneda'


class Promocion(models.Model):
    idpromocion = models.BigAutoField(primary_key=True)
    imagenpromocion = models.ImageField(upload_to='promocion/')  # Field name made lowercase. This field type is a guess.
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Promocion'


class Tblcarrito(models.Model):
    idusuario = models.OneToOneField(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    preciototal = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'TblCarrito'


class Tblitem(models.Model):
    codigosku = models.CharField(db_column='codigoSKU', unique=True, max_length=25)  # Field name made lowercase.
    #pliegues = models.CharField(max_length=20, blank=True, null=True)
    stock = models.IntegerField()
    descripcion = models.TextField()
    idproduct = models.BigAutoField(primary_key=True)
    #rangovelocidad = models.CharField(max_length=20, blank=True, null=True)
    destacado = models.BooleanField()
    agotado = models.BooleanField(blank=True, null=True)
    nuevoproducto = models.BooleanField()
    preciorebajado = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        validators=[MinValueValidator(0)], blank=True, null=True)  # This field type is a guess.
    precionormal = models.DecimalField(
        max_digits=20, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )  # This field type is a guess.
    imagenprincipal= models.ImageField(upload_to='imagenPrincipalItem/', blank=True, null=True)
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    #idmarca = models.ForeignKey(Marca, models.DO_NOTHING, db_column='id', blank=True, null=True)

    class Meta:
        db_table = 'TblItem'


class Tblnoticia(models.Model):
    estado = models.IntegerField()
    idnoticia = models.BigAutoField(db_column='idNoticia', primary_key=True)  # Field name made lowercase.
    imagennoticia = models.TextField(db_column='imagenNoticia')  # Field name made lowercase. This field type is a guess.
    descripcion = models.TextField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TblNoticia'


class Tblpedido(models.Model):
    idpedido = models.BigAutoField(primary_key=True)
    idcliente = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='idCliente')  # Field name made lowercase.
    subtotal = models.TextField()  # This field type is a guess.
    direcciondestino = models.TextField()
    total = models.TextField()  # This field type is a guess.
    igv = models.FloatField(blank=True, null=True)
    totaldescuento = models.FloatField()
    idcupon = models.ForeignKey(Cupon, models.DO_NOTHING, db_column='idCupon', blank=True, null=True)  # Field name made lowercase.
    idmoneda = models.ForeignKey(Moneda, models.DO_NOTHING, db_column='idmoneda')
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TblPedido'


class Tblslider(models.Model):
    id = models.BigAutoField(primary_key=True)
    imagen = models.ImageField(upload_to='slider/')
    descripcion = models.TextField(blank=True, null=True)
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TblSlider'

class CustomUserManager(BaseUserManager):
    def create_user(self, nombreusuario, password=None, **extra_fields):
        # Verifica que el campo nombreusuario esté presente
        if not nombreusuario:
            raise ValueError('El campo nombreusuario debe ser declarado')
        
        # Crea el usuario con el nombre de usuario y otros campos extra
        user = self.model(nombreusuario=nombreusuario, **extra_fields)
        
        # Establece la contraseña
        if password:
            user.set_password(password)
        
        # Guarda el usuario en la base de datos
        user.save(using=self._db)
        return user

    def create_superuser(self, nombreusuario, password=None, **extra_fields):
        # Establece is_staff y is_superuser para el superusuario
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Llama a create_user para crear el superusuario
        return self.create_user(nombreusuario, password, **extra_fields)

class CustomUser(AbstractUser):
    # Eliminar el campo `username` heredado
    username = None
    
    # Campos adicionales
    nombre = models.CharField(max_length=128, blank=True, null=True)
    apellidos = models.CharField(max_length=128, blank=True, null=True)
    nombreusuario = models.CharField(max_length=128, unique=True)  # Usamos nombreusuario para autenticación
    direccion = models.CharField(max_length=128, blank=True, null=True)
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    imagenperfil = models.ImageField(upload_to='perfilUsuarioimagen/', blank=True, null=True)

    
    departamento = models.CharField(max_length=128, blank=True, null=True)
    provincia = models.CharField(max_length=128, blank=True, null=True)
    distrito = models.CharField(max_length=128, blank=True, null=True)
    
    
    email_verified_at = models.DateTimeField(blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)

    # Especificar que el campo para autenticar es `nombreusuario`
    USERNAME_FIELD = 'nombreusuario'
    
    # Campos requeridos adicionales (no necesitas username ya que lo has reemplazado con nombreusuario)
    REQUIRED_FIELDS = ['email']  # En Django, `email` es un campo por defecto si lo estás usando como required

    # Manager personalizado
    objects = CustomUserManager()
    
    def __str__(self):
        return self.nombreusuario
    def get_full_name(self):
        return f"{self.nombre} {self.apellidos or ''}".strip()



class Tipocambio(models.Model):
    tipocambio = models.BigIntegerField(blank=True, null=True)
    idcambio = models.BigAutoField(primary_key=True)
    idmoneda = models.ForeignKey(Moneda, models.DO_NOTHING, db_column='idmoneda', blank=True, null=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'TipoCambio'


class Valoracion(models.Model):
    estrellas = models.BigIntegerField(blank=True, null=True)
    comentario = models.TextField()
    idvaloracion = models.BigAutoField(primary_key=True)
    estado = models.BigIntegerField()
    telefono = models.BigIntegerField(blank=True, null=True)
    idproduct = models.ForeignKey(Tblitem, models.DO_NOTHING, db_column='idproduct', blank=True, null=True)
    iduser = models.ForeignKey(settings.AUTH_USER_MODEL ,models.DO_NOTHING, db_column='idUser', blank=True, null=True)  # Field name made lowercase.
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Valoracion'


class Tbldetallecarrito(models.Model):
    idproduct = models.OneToOneField(Tblitem, models.DO_NOTHING, db_column='idproduct', primary_key=True)
    isuser = models.ForeignKey(Tblcarrito, models.DO_NOTHING, db_column='isUser')  # Field name made lowercase.
    cantidad = models.BigIntegerField()
    idcupon = models.ForeignKey(Cupon, models.DO_NOTHING, db_column='idCupon', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'tblDetalleCarrito'
        unique_together = (('idproduct', 'isuser'),)


class Tblimagenitem(models.Model):
    idimagen = models.BigAutoField(db_column='idImagen', primary_key=True)  # Field name made lowercase.
    idproduct = models.ForeignKey(Tblitem, models.DO_NOTHING, db_column='idproduct', blank=True, null=True)
    imagen = models.ImageField(upload_to='imagenesitem/') # This field type is a guess.
    estado = models.IntegerField()

    class Meta:
        db_table = 'tblImagenItem'


class Tblitemclase(models.Model):
    idclase = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)

    class Meta:
        db_table = 'tblItemClase'

class Tblitempropiedad(models.Model):
    idpropiedad = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    idclase = models.ForeignKey(Tblitemclase, models.DO_NOTHING, db_column='idclase', blank=True, null=True)
    icono = models.FileField(upload_to='iconoProiedad/', blank=True, null=True)

    class Meta:
        db_table = 'tblItemPropiedad'
        
class Tblitemclasepropiedad(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    idproduct = models.ForeignKey(Tblitem, models.DO_NOTHING, db_column='idproduct', related_name='clases_propiedades')
    idpropiedad = models.ForeignKey(Tblitempropiedad, models.DO_NOTHING, db_column='idpropiedad', blank=True, null=True)
    idclase = models.ForeignKey(Tblitemclase, models.DO_NOTHING, db_column='idclase', blank=True, null=True)

    class Meta:
        db_table = 'tblItemClasePropiedad'





class Tblitemrelacionado(models.Model):
    idproduct = models.ForeignKey(Tblitem, models.DO_NOTHING, db_column='idproduct', blank=True, null=True)
    id = models.BigAutoField(primary_key=True)
    fk = models.ForeignKey('self', models.DO_NOTHING, db_column='FK_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'tblItemRelacionado'


class Tbldetallepedido(models.Model):
    idpedido = models.OneToOneField(Tblpedido, models.DO_NOTHING, db_column='idpedido', primary_key=True)
    idproduct = models.ForeignKey(Tblitem, models.DO_NOTHING, db_column='idproduct')
    cantidad = models.IntegerField()
    preciototal = models.TextField()  # This field type is a guess.
    preciunitario = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'tbldetallepedido'
        unique_together = (('idpedido', 'idproduct'),)

class Administracion(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombreempresa = models.BigIntegerField()
    ruc = models.BigIntegerField()
    telefono = models.BigIntegerField()
    igv = models.BigIntegerField()
    idmoneda = models.ForeignKey(Moneda, models.DO_NOTHING, db_column='idmoneda', blank=True, null=True)
    
    datospasarela = models.TextField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Administracion'
