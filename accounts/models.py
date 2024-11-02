from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from helpers.models import TrackingModel
from django.contrib.auth.models import UserManager


class MyUserManager(UserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        Verilen istifadəçi adı, e-posta və parol ilə bir istifadəçi yaradın və saxlayın.
        """
        if not username:
            # raise ValueError("The given username must be set")
            raise ValueError("Verilmiş istifadəçi adı müəyyən edilməlidir.")

        if not email:
            # raise ValueError("The given email must be set")
            raise ValueError("Verilmiş e-posta müəyyən edilməlidir.")

        # İstifadəçi adı yoxlanilmasi: Əgər verilmiş istifadəçi adı artıq bazada mövcuddursa,
        if self.model.objects.filter(username=username).exists():
            raise ValueError(_("Bu istifadəçi adı artıq götürülüb."))

        # İstifadəçi bloklanmışsa, xətanı atın
        if extra_fields.get("is_blocked"):
            raise ValueError(_("Bloklanmış istifadəçi, hesabını yarada bilməz."))

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        # İstifadəçi adı yoxlanilmasi: Əgər verilmiş istifadəçi adı artıq bazada mövcuddursa,
        if self.model.objects.filter(username=username).exists():
            raise ValueError(_("Bu istifadəçi adı artıq götürülüb."))

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, TrackingModel):

    AREA_OF_USE_CHOICES = [
        ("mekteb", "Məktəb"),
        ("universitet", "Universitet"),
        ("senedler", "Sənədlər"),
        ("blog", "Blog"),
        ("tercume", "Tərcümə"),
        ("marketinq", "Marketinq"),
    ]

    AZERBAIJAN_REGIONS = [
        ("absheron", "Abşeron"),
        ("agcabedi", "Ağcabədi"),
        ("agdam", "Ağdam"),
        ("agdash", "Ağdaş"),
        ("agstafa", "Ağstafa"),
        ("agsu", "Ağsu"),
        ("astara", "Astara"),
        ("baku", "Bakı"),
        ("balaken", "Balakən"),
        ("barda", "Bərdə"),
        ("beylagan", "Beyləqan"),
        ("bilasuvar", "Biləsuvar"),
        ("dashkasan", "Daşkəsən"),
        ("fuzuli", "Füzuli"),
        ("gadabay", "Gədəbəy"),
        ("ganja", "Gəncə"),
        ("goranboy", "Goranboy"),
        ("goychay", "Göyçay"),
        ("goygol", "Göygöl"),
        ("hajigabul", "Hacıqabul"),
        ("imisli", "İmişli"),
        ("ismayilli", "İsmayıllı"),
        ("jabrayil", "Cəbrayıl"),
        ("jalilabad", "Cəlilabad"),
        ("kalbajar", "Kəlbəcər"),
        ("khachmaz", "Xaçmaz"),
        ("khizi", "Xızı"),
        ("khojali", "Xocalı"),
        ("kurdamir", "Kürdəmir"),
        ("lachin", "Laçın"),
        ("lankaran", "Lənkəran"),
        ("lerik", "Lerik"),
        ("masally", "Masallı"),
        ("mingachevir", "Mingəçevir"),
        ("nakhchivan", "Naxçıvan"),
        ("neftchala", "Neftçala"),
        ("oguz", "Oğuz"),
        ("ordubad", "Ordubad"),
        ("qabala", "Qəbələ"),
        ("qakh", "Qax"),
        ("qazakh", "Qazax"),
        ("qusar", "Qusar"),
        ("sabirabad", "Sabirabad"),
        ("salyan", "Salyan"),
        ("samukh", "Samux"),
        ("shabran", "Şabran"),
        ("shaki", "Şəki"),
        ("shamakhi", "Şamaxı"),
        ("shamkir", "Şəmkir"),
        ("shirvan", "Şirvan"),
        ("shusha", "Şuşa"),
        ("siazan", "Siyəzən"),
        ("sumqayit", "Sumqayıt"),
        ("tartar", "Tərtər"),
        ("tovuz", "Tovuz"),
        ("yardimli", "Yardımlı"),
        ("yevlakh", "Yevlax"),
        ("zangilan", "Zəngilan"),
        ("zardab", "Zərdab"),
        # Digər rayonları da əlavə edə bilərsiniz
    ]

    phone_regex = RegexValidator(
        regex=r"^\+?[0-9]{9,20}$",
        message="Telefon nömrəsi '+994775685605' formatında olmalıdır.",
    )

    username = models.CharField(
        max_length=20,
        unique=True,
        error_messages={
            "max_length": _("İstifadəçi adı ən çox 20 simvol olmalıdır."),
            "unique": _("Bu istifadəçi adı artıq götürülüb."),
            "blank": _("İstifadəçi adı sahəsi boş qala bilməz."),
            "null": _("İstifadəçi adı sahəsi boş qala bilməz."),
        },
    )
    first_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        error_messages={
            "max_length": _("Ad ən çox 30 simvol olmalıdır."),
            "blank": _("Ad sahəsi boş qala bilməz."),
            "null": _("Ad sahəsi boş qala bilməz."),
        },
    )
    last_name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        error_messages={
            "max_length": _("Soyad ən çox 30 simvol olmalıdır."),
            "blank": _("Soyad sahəsi boş qala bilməz."),
            "null": _("Soyad sahəsi boş qala bilməz."),
        },
    )
    email = models.EmailField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        error_messages={
            "max_length": _("E-posta ən çox 50 simvol olmalıdır."),
            "blank": _("E-posta sahəsi boş qala bilməz."),
            "null": _("E-posta sahəsi boş qala bilməz."),
            "invalid": _("Keçərli bir e-posta ünvanı daxil edin."),
        },
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        error_messages={
            "max_length": _("Telefon nömrəsi ən çox 15 simvol olmalıdır."),
            "unique": _("Bu telefon nömrəsi artıq götürülüb."),
            "blank": _("Telefon nömrəsi sahəsi boş qala bilər."),
            "null": _("Telefon nömrəsi sahəsi boş qala bilər."),
            "invalid": _("Keçərli bir telefon nömrəsi daxil edin."),
        },
    )

    area_of_use = models.CharField(
        max_length=20, choices=AREA_OF_USE_CHOICES, default="mekteb", blank=True
    )

    ## Yeni sahələr
    daily_session = models.IntegerField(default=0, verbose_name="Günlük Sessiya")
    is_blocked = models.BooleanField(default=False, verbose_name="Bloklanıb")

    ## Yeni `location_city` sahəsi
    location_city = models.CharField(
        max_length=50,
        choices=AZERBAIJAN_REGIONS,
        blank=True,
        null=True,
        verbose_name="Məkan (Rayon)",
    )

    verify = models.BooleanField(default=False, verbose_name="Təsdiqlənib")
    verification_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Təsdiq Kodu")

    ## İstifadəçi identifikasiyası üçün username əvəzinə email istifadə olunacaq
    objects = MyUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.username
