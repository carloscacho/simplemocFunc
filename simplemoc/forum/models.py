from django.db import models
from django.conf import settings
#libs
from taggit.managers import TaggableManager

# model

class Thread(models.Model):
    title = models.CharField('Titulo', max_length=100)
    slug = models.SlugField('Identificador', max_length=100, unique=True)
    
    body = models.TextField('Mensagem')
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='threads',
        on_delete=models.CASCADE
        )
    #atributos de consulta
    views = models.IntegerField('Visualizações', blank=True, default=0)
    answers = models.IntegerField('Respostas', blank=True, default=0)
    tags = TaggableManager()

    #atributos de auditoria
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    @models.permalink
    def get_absolute_url(self): 
        return ('forum_thread',(), {'slug': self.slug})


    def __str__(self):
        return self.title

    class Meta:
        verbose_name= 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']


class Replay(models.Model):
    thread = models.ForeignKey(
        Thread, 
        verbose_name='tópico',
        related_name='replies',
        on_delete=models.CASCADE
        )
    replay = models.TextField('Resposta')
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Autor',
        related_name='replies',
        on_delete=models.CASCADE
        )
        
    correct = models.BooleanField('Correta?', blank=True, default=False)

    replay_up = models.IntegerField('Positiva', blank=True, default=0)
    replay_down = models.IntegerField('Negativa', blank=True, default=0)

    #atributos de auditoria
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.replay
    
    class Meta:
        verbose_name= 'Reposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', '-replay_up', 'replay_down', 'created']

# contabilizar o numero de respostas
def post_save_replay(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.replies.exclude(pk=instance.pk).update(
            correct=False
        )

def post_delete_replay(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()

models.signals.post_save.connect(
    post_save_replay, sender=Replay, dispatch_uid='post_save_replay'
)

models.signals.post_delete.connect(
    post_delete_replay, sender=Replay, dispatch_uid='post_delete_replay'
)