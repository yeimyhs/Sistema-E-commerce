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
    activo = models.BooleanField(default =1)
    idcupon = models.BigAutoField(db_column='idCupon', primary_key=True)  # Field name made lowercase.
    cantidaddescuento = models.FloatField()
    
    TIPO_DESCUENTO_CHOICES = [
        ('DINERO', 'Dinero'),
        ('PORCENTAJE', 'Porcentaje'),
    ]
    tipocupon = models.CharField(
        max_length=10,
        choices=TIPO_DESCUENTO_CHOICES,
        verbose_name="Tipo de Cupon"
    )
    
    codigo = models.CharField(max_length=128)
    fechavigencia = models.DateTimeField(blank=True, null=True)
    fechacaducacion = models.DateTimeField(blank=True, null=True)
    
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Cupon'

#------------------------------------------------------------------
class Marca(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    imagen = models.ImageField(upload_to='marca/', blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'Marca'
        

class Tblcategoria(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    
    #imagen = models.ImageField(upload_to='Categoria/', blank=True, null=True)  # This field type is a guess.
    imagen = models.FileField(upload_to='iconoProiedad/', blank=True, null=True)

    class Meta:
        db_table = 'TblCategoria'

class tblitemcategoria(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(db_column='tblitemcategoria', primary_key=True)  # Field name made lowercase.
    iditem = models.ForeignKey('Tblitem', on_delete=models.CASCADE, db_column='iditem', related_name='categoria_relacionada')
    idcategoria = models.ForeignKey(Tblcategoria, on_delete=models.CASCADE, db_column='idcategoria')

    class Meta:
        db_table = 'tblitemcategoria'

        
        
class Tblmodelo(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    idmarca = models.ForeignKey(Marca, models.DO_NOTHING, db_column='idmarca', blank=True, null=True)

    class Meta:
        db_table = 'TblModelo'


class Moneda(models.Model):
    activo = models.BooleanField(default =1)
    idmoneda = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Moneda'


class Promocion(models.Model):
    activo = models.BooleanField(default =1)
    idpromocion = models.BigAutoField(primary_key=True)
    imagenpromocion = models.ImageField(upload_to='promocion/')  # Field name made lowercase. This field type is a guess.
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Promocion'


class Tblcarrito(models.Model):
    activo = models.BooleanField(default =1)
    idusuario = models.OneToOneField(settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    preciototal = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'TblCarrito'


class Tblitem(models.Model):
    activo = models.BooleanField(default =1)
    codigosku = models.CharField(db_column='codigoSKU', unique=True, max_length=25)  # Field name made lowercase.
    #pliegues = models.CharField(max_length=20, blank=True, null=True)
    titulo = models.CharField(max_length=128)
    stock = models.IntegerField()
    descripcion = models.TextField()
    idproduct = models.BigAutoField(primary_key=True)
    #rangovelocidad = models.CharField(max_length=20, blank=True, null=True)
    destacado = models.BooleanField()
    agotado = models.BooleanField(blank=True, null=True)
    nuevoproducto = models.BooleanField()
    preciorebajado = models.DecimalField(
        max_digits=20, 
        decimal_places=2, blank=True, null=True)  # This field type is a guess.
    precionormal = models.DecimalField(max_digits=20, decimal_places=2)  # This field type is a guess.
    imagenprincipal= models.ImageField(upload_to='imagenPrincipalItem/', blank=True, null=True)
    fechapublicacion = models.DateTimeField()
    peso = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)  # This field type is a guess.
    altura = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)  # This field type is a guess.
    profundidad = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)  # This field type is a guess.
    ancho = models.DecimalField(max_digits=20, decimal_places=2,blank=True, null=True)  # This field type is a guess.
    
    
    estado = models.IntegerField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    idmodelo = models.ForeignKey(Tblmodelo, models.DO_NOTHING, db_column='idmodelo', blank=True, null=True)

    class Meta:
        db_table = 'TblItem'


class Tblnoticia(models.Model):
    activo = models.BooleanField(default =1)
    estado = models.IntegerField()
    idnoticia = models.BigAutoField(db_column='idNoticia', primary_key=True)  # Field name made lowercase.
    titulo = models.CharField(max_length=225)
    imagennoticia = models.ImageField(upload_to='imagenNoticia/', blank=True, null=True)
# Field name made lowercase. This field type is a guess.
    descripcion = models.TextField()
    fechapublicacion = models.DateTimeField()
    
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TblNoticia'


class Tblpedido(models.Model):
    activo = models.BooleanField(default =1)
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


class TblCarrusel(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(primary_key=True)
    imagen = models.ImageField(upload_to='slider/')
    titulo = models.CharField(max_length=225)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.IntegerField()
    fechapublicacion = models.DateTimeField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TblCarrusel'

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
    activo = models.BooleanField(default =1)
    
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
    activo = models.BooleanField(default =1)
    #tipocambio = models.DecimalField(max_digits=22, decimal_places=22,blank=True, null=True)
    tipocambio = models.DecimalField(
        max_digits=20, 
        decimal_places=2, blank=True, null=True)  # This field type is a guess.
    
    idcambio = models.BigAutoField(primary_key=True)
    idmoneda = models.ForeignKey(Moneda, models.DO_NOTHING, db_column='idmoneda', blank=True, null=True)
    fecha = models.DateTimeField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'TipoCambio'

class Tblsede(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, verbose_name="Celular o Teléfono")

    email = models.EmailField(verbose_name="Correo Electrónico")
    imagen = models.ImageField(upload_to='imagenessede/',blank=True, null=True) # This field type is a guess.

    
    class Meta:
        db_table = 'Tblsede'

class Tblreclamacion(models.Model):
    TIPOS_ID = [
        ('DNI', 'DNI'),
        ('RUC', 'RUC')
    ]

    tipoid = models.CharField(
        max_length=25,  # Elige un valor adecuado para los códigos más largos
        choices=TIPOS_ID
    )
    nroid = models.BigIntegerField()
    idsede = models.ForeignKey(Tblsede, models.DO_NOTHING, blank=True, null=True)
    
    email = models.EmailField(verbose_name="Correo Electrónico")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido_paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    telefono = models.CharField(max_length=20, verbose_name="Celular o Teléfono")
    departamento = models.CharField(max_length=100, verbose_name="Departamento")
    provincia = models.CharField(max_length=100, verbose_name="Provincia")
    distrito = models.CharField(max_length=100, verbose_name="Distrito")
    direccion = models.TextField(verbose_name="Dirección")
    TIPO_BIEN_CHOICES = [
        ('PRODUCTO', 'Producto'),
        ('SERVICIO', 'Servicio'),
    ]
    tipo_bien = models.CharField(
        max_length=10,
        choices=TIPO_BIEN_CHOICES,
        verbose_name="Tipo de Bien Contratado"
    )
    numero_pedido = models.CharField(max_length=50, verbose_name="Número de Pedido", blank=True, null=True)
    monto_pedido = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto del Pedido")
    descripcion_bien = models.TextField(verbose_name="Descripción del Bien Contratado")
    TIPO_RECLAMO_CHOICES = [
        ('RECLAMO', 'Reclamo'),
        ('QUEJA', 'Queja'),
    ]

    tipo_reclamo = models.CharField(
        max_length=10,
        choices=TIPO_RECLAMO_CHOICES,
        verbose_name="Tipo de Reclamo"
    )
    descripcion_reclamo = models.TextField(verbose_name="Descripción del Reclamo o Queja")
    pedido_consumidor = models.TextField(verbose_name="Pedido del Consumidor")


    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default =1)
    estado = models.IntegerField(default = 0)
    comentario = models.TextField(blank=True, null=True)


class Valoracion(models.Model):
    activo = models.BooleanField(default =1)
    estrellas = models.BigIntegerField(blank=True, null=True)
    comentario = models.TextField()
    idvaloracion = models.BigAutoField(primary_key=True)
    estado = models.BigIntegerField()
    idproduct = models.ForeignKey(Tblitem, models.DO_NOTHING, db_column='idproduct', blank=True, null=True)
    iduser = models.ForeignKey(settings.AUTH_USER_MODEL ,models.DO_NOTHING, db_column='idUser', blank=True, null=True)  # Field name made lowercase.
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Valoracion'


class Tbldetallecarrito(models.Model):
    activo = models.BooleanField(default =1)
    idproduct = models.OneToOneField(Tblitem, models.DO_NOTHING, db_column='idproduct', primary_key=True)
    isuser = models.ForeignKey(Tblcarrito, models.DO_NOTHING, db_column='isUser')  # Field name made lowercase.
    cantidad = models.BigIntegerField()
    idcupon = models.ForeignKey(Cupon, models.DO_NOTHING, db_column='idCupon', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'tblDetalleCarrito'
        unique_together = (('idproduct', 'isuser'),)


class Tblimagenitem(models.Model):
    activo = models.BooleanField(default =1)
    idimagen = models.BigAutoField(db_column='idImagen', primary_key=True)  # Field name made lowercase.
    idproduct = models.ForeignKey(Tblitem, models.DO_NOTHING, db_column='idproduct', blank=True, null=True)
    imagen = models.ImageField(upload_to='imagenesitem/') # This field type is a guess.
    estado = models.IntegerField()

    class Meta:
        db_table = 'tblImagenItem'


class Tblitemclase(models.Model):
    activo = models.BooleanField(default =1)
    idclase = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)

    class Meta:
        db_table = 'tblItemClase'

class Tblitempropiedad(models.Model):
    activo = models.BooleanField(default =1)
    idpropiedad = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=128)
    idclase = models.ForeignKey(Tblitemclase, models.DO_NOTHING, db_column='idclase', blank=True, null=True)
    icono = models.FileField(upload_to='iconoProiedad/', blank=True, null=True)

    class Meta:
        db_table = 'tblItemPropiedad'
        
class tblitemclasevinculo(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    iditem = models.ForeignKey(Tblitem, on_delete=models.CASCADE, db_column='iditem', related_name='clases_propiedades')
    propiedad = models.CharField(max_length=225)
    idclase = models.ForeignKey(Tblitemclase, on_delete=models.CASCADE, db_column='idclase')

    class Meta:
        db_table = 'tblItemClaseVinculo'


class tblitemcupon(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    iditem = models.ForeignKey(Tblitem, models.DO_NOTHING, db_column='iditem', related_name='cupon_relacionado')
    idcupon = models.ForeignKey(Cupon, models.DO_NOTHING, db_column='idcupon', blank=True, null=True)

    class Meta:
        db_table = 'tblItemCupon'




class Tblitemrelacionado(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(primary_key=True)
    item = models.ForeignKey(Tblitem, related_name='relacionados', on_delete=models.CASCADE)
    item_relacionado = models.ForeignKey(Tblitem, related_name='relacionados_por', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.item == self.item_relacionado:
            raise ValidationError('Un item no puede estar relacionado consigo mismo.')
        super().save(*args, **kwargs)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['item', 'item_relacionado'], name='unique_item_relacion')
        ]
        
class Tbldetallepedido(models.Model):
    activo = models.BooleanField(default =1)
    idpedido = models.OneToOneField(Tblpedido, models.DO_NOTHING, db_column='idpedido', primary_key=True)
    idproduct = models.ForeignKey(Tblitem, models.DO_NOTHING, db_column='idproduct')
    cantidad = models.IntegerField()
    preciototal = models.TextField()  # This field type is a guess.
    preciunitario = models.TextField()  # This field type is a guess.

    class Meta:
        db_table = 'tbldetallepedido'
        unique_together = (('idpedido', 'idproduct'),)

class Administracion(models.Model):
    activo = models.BooleanField(default =1)
    id = models.BigAutoField(primary_key=True)
    nombreempresa = models.CharField(max_length=128)
    ruc = models.BigIntegerField()
    telefono = models.BigIntegerField()
    igv = models.BigIntegerField()
    idmoneda = models.ForeignKey(Moneda, models.DO_NOTHING, db_column='idmoneda', blank=True, null=True)
    
    datospasarela = models.TextField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Administracion'
