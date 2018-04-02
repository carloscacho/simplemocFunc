from django.db import models
from django.conf import settings
#libs
from taggit.managers import TaggableManager

# model

class Thread(models.Model):
    title = models.CharField('Titulo', max_length=100)
    
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

    def __str__(self):
        return self.title

    class Meta:
        verbose_name= 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-modified']


class Replay(models.Model):
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
        verbose_name= 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-correct', 'replay_up', 'created']