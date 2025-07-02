from django.db import models

class TypePdf(models.Model):
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class Pdf(models.Model):
    pdf = models.URLField(max_length=255)
    id_post = models.ForeignKey('marketplace.Post', on_delete=models.CASCADE)
    id_user = models.ForeignKey('marketplace.User', on_delete=models.CASCADE)
    id_type_pdf = models.ForeignKey('marketplace.TypePdf', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

