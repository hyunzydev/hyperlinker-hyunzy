from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class WebLink(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    category = models.CharField(
        max_length=50,
        choices=[
            ("personal", "개인 즐겨찾기"),
            ("work", "업무 활용 자료"),
            ("reference", "참고 자료"),
            ("education", "교육 및 학습 자료"),
        ],
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="weblinks"
    )
    shared_with = models.ManyToManyField(
        User, related_name="received_weblinks", blank=True
    )
    write_permissions = models.ManyToManyField(
        User, related_name="write_weblinks", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            existing_link = WebLink.objects.filter(id=self.pk).first()
            if existing_link:
                # 기존에 공유된 정보 유지
                self.shared_with.set(existing_link.shared_with.all())
                self.write_permissions.set(existing_link.write_permissions.all())

        super().save(*args, **kwargs)

