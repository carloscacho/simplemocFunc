from django.db import models
from django.conf import settings
from simplemoc.core.mail import send_mail_template
from django.utils import timezone

# Create your models here.
class CourseManager(models.Manager):

	def search(self, query):
		return self.get_queryset().filter(
			models.Q(name__icontains=query) |
			models.Q(description__icontains= query)
			)

class Course(models.Model):

	name = models.CharField('Nome', max_length=50)
	slug = models.SlugField('Atalho')
	description =  models.TextField(
		'Descrição', blank=True
		)

	about = models.TextField('Sobre o Curso',
		blank = True
		)
	
	start_date = models.DateField(
		'Data de Inicio', null=True, blank=True
		 )

	image = models.ImageField(
		upload_to='courses/images', verbose_name='Imagem',
		null=True, blank=True
		)

	created_at  = models.DateTimeField(
		'Criado em', auto_now_add=True
		)

	updated_at = models.DateTimeField(
    	'Atualizado em', auto_now=True
    	)

	objects = CourseManager()

	def __str__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return ('details', (), {'slug': self.slug})
	
	def release_lessons(self):
		today = timezone.now().date()
		return self.lessons.filter(relase_date__lte=today)

	class Meta:
		verbose_name='Curso'
		verbose_name_plural='Cursos'
		ordering = ['name']

'''
Modelo das lições que são ligadas a um curso e possuiem materias 
'''
class Lesson(models.Model):
	name = models.CharField('Nome', max_length=100)

	description = models.TextField('Descrição', blank=True)

	number = models.IntegerField('ordem', blank=True, default=0)

	relase_date = models.DateField('data de liberação', blank=True, null=True)

	course = models.ForeignKey(Course, 
		verbose_name='Curso', related_name='lessons', on_delete=models.CASCADE)

	created_at  = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)


	def __str__(self):
		return self.name

	#verifica se as aulas já estão disponiveis
	def is_available(self):
		if self.relase_date:
			today = timezone.now().date()
			return self.relase_date <= today
		return False


	class Meta:
		verbose_name='Aula'
		verbose_name_plural='Aulas'
		ordering=['number']


class Material(models.Model):
	name = models.CharField('Nome', max_length=100)
	embendded  = models.TextField('Video da aula', blank=True)
	is_embendded  = models.BooleanField('é um video?', default=False)
	file = models.FileField(upload_to='lessons/materials', blank=True, null=True)
	
	lesson = models.ForeignKey(Lesson, verbose_name='Aula', 
		related_name='materials', on_delete=models.CASCADE)

	created_at  = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField('Atualizado em', auto_now=True)


	def __str__(self):
		return self.name

	class Meta:
		verbose_name='Material'
		verbose_name_plural='Materiais'

class Enrollment(models.Model):

	STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'cancelado'),)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, 
    	verbose_name='Usuário',
    	related_name='enrollments',
		on_delete=models.CASCADE
    	)

	course = models.ForeignKey(
    	Course, 
    	verbose_name='Curso',
    	related_name='enrollments',
		on_delete=models.CASCADE
    	)

	status = models.IntegerField('Situação',
   		choices=STATUS_CHOICES, default=0, blank=True)

	created_at  = models.DateTimeField(
		'Criado em', auto_now_add=True
		)

	updated_at = models.DateTimeField(
    	'Atualizado em', auto_now=True
    	)


	def active(self):
		self.status = 1
		self.save()
		
	def is_approved(self):
		return self.status == 1

	class Meta:
   		verbose_name='Inscrição'
   		verbose_name_plural='Inscrições'
   		unique_together = (('user', 'course'),)
   			

class Announcement(models.Model):
    """
    Description: Model Description
    """
    course = models.ForeignKey(Course,
		verbose_name='Curso', related_name='announcements', on_delete=models.CASCADE)
    title = models.CharField('Titulo', max_length=100)
    content = models.TextField('Conteúdo')

    created_at  = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)


    def __str__(self):
    	return self.title

    class Meta:
    	verbose_name='Anuncio'
    	verbose_name_plural='Anuncios'
    	ordering=['-created_at']
# modelo do banco dos commentarios
class Comment(models.Model):
    """
    Description: Model Description
    """
    announcement = models.ForeignKey(Announcement, verbose_name='Aula',
    	related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário', on_delete=models.CASCADE)

    comment = models.TextField('Comentário')

    created_at  = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name='Comentário'
        verbose_name_plural='Comentários'
        ordering=['created_at']
'''
Quando um novo anuncio é criado todos os usuarios que estão
inscritos no curso recebem um email
'''
def post_save_announcement(instance, created, **kwargs):
	if created:
	    subject = instance.title
	    context = {
	    	'announcement': instance
	    }

	    template_name = 'courses/announcement_mail.html'
	    users = Enrollment.objects.filter(course=instance.course, status=1)
	    for user in users:
	    	recipient_list = [user.user.email]
	    	send_mail_template(subject,template_name,context, recipient_list)
#vinculação do metodo com signals para que 
#a criação de um anuncio seja realizado o envio dos emails
models.signals.post_save.connect(
	post_save_announcement, sender=Announcement,
	dispatch_uid='post_save_announcement')


