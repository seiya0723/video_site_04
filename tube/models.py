from django.db import models
from django.utils import timezone


import uuid 


class Category(models.Model):

    class Meta:
        db_table = "category"


    #TIPS:数値型の主キーではPostgreSQLなど一部のDBでエラーを起こす。それだけでなく予測がされやすく衝突しやすいので、UUID型の主キーに仕立てる。
    id      = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False )
    name    = models.CharField(verbose_name="カテゴリ名",max_length=20)
    
    def __str__(self):
        return self.name


#実際には動画サイトで多対多を実装する時、良いね悪いねの評価等に使う。タグはハッシュタグとして扱うほうがよい。
class Tag(models.Model):

    class Meta:
        db_table = "tag"

    id      = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False )
    name    = models.CharField(verbose_name="タグ名",max_length=20)
    
    def __str__(self):
        return self.name



class Video(models.Model):

    class Meta:
        db_table = "video"

    id      = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False )
    title   = models.CharField(verbose_name="タイトル", max_length=30)

    #TIPS:Categoryに登録されているデータのidを入力する外部キー。カテゴリが削除される時、そのカテゴリを含むデータがある場合、削除されない(models.PROTECT)
    category    = models.ForeignKey(Category,verbose_name="カテゴリ",on_delete=models.PROTECT)

    #TIPS:タグは複数選ぶのでManyToManyFieldとする。マイグレーション時、タグとビデオを繋げる中間テーブルが作られる。
    tag         = models.ManyToManyField(Tag,verbose_name="タグ",blank=True)

    
    comment = models.CharField(verbose_name="動画説明文", max_length=2000)
    dt      = models.DateTimeField(verbose_name="投稿日", default=timezone.now)
    edited  = models.BooleanField(default=False)
    image   = models.ImageField(verbose_name="画像",upload_to="tube/image",blank=True)
    movie     = models.FileField(verbose_name="動画",upload_to="tube/movie",blank=True)

    def __str__(self):
        return self.title


#TODO:ForeiginKeyを使ってVideoに対してコメントを投稿するCommentクラスを作る。

