from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Zone(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name=u'逻辑删除标志')
    name = models.CharField(max_length=255, verbose_name=u'名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    delete_time = models.DateTimeField(null=True, verbose_name=u'删除时间')

    class Meta:
        db_table = 'zone'


class User(AbstractBaseUser, PermissionsMixin):
    zone = models.ForeignKey(
        Zone,null=True,default=1,
        on_delete=models.CASCADE,
    )
    telephone = models.CharField(max_length=11, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    objects = UserManager()

    class Meta:
        db_table = 'user'



class Patient(models.Model):
    zone = models.ForeignKey(
        Zone,
        null=True,
        on_delete=models.CASCADE,
        default=1,
    )
    is_delete = models.BooleanField(default=False, verbose_name=u'逻辑删除标志')
    name = models.CharField(max_length=255, verbose_name=u'姓名')
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default="Untitled.png", verbose_name=u'头像')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    delete_time = models.DateTimeField(null=True, verbose_name=u'删除时间')

    class Meta:
        db_table = 'patient'

    def get_image(self):
        return self.profile_image.url if self.profile_image else ''


class ExaminationType(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name=u'逻辑删除标志')
    name = models.CharField(max_length=255, verbose_name=u'RTL，CSA，AI')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    delete_time = models.DateTimeField(null=True, verbose_name=u'删除时间')

    class Meta:
        db_table = 'examination_type'


class Examination(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
    )
    examination_type = models.ForeignKey(
        ExaminationType,
        on_delete=models.CASCADE,
    )
    result = models.CharField(max_length=255, verbose_name=u'RTL，CSA，AI')
    input_image = models.ImageField(upload_to='inputs/', blank=True, verbose_name=u'检测图片')
    output_image = models.ImageField(upload_to='outputs/', blank=True, verbose_name=u'输出图片')
    is_delete = models.BooleanField(default=False, verbose_name=u'逻辑删除标志')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name=u'更新时间')
    delete_time = models.DateTimeField(null=True, verbose_name=u'删除时间')

    class Meta:
        db_table = 'examination'
