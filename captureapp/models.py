from django.db import models
# accountsアプリのmodelsモジュールからCustomUserをインポート
from accounts.models import CustomUser

class Category(models.Model):
    '''投稿する写真のカテゴリを管理するモデル
    '''
    # カテゴリ名のフィールド
    title = models.CharField(
        verbose_name='学年・クラス', # フィールドのタイトル
        max_length=20)
    
    def __str__(self):
        '''オブジェクトを文字列に変換して返す
        
        Returns(str):カテゴリ名
        '''
        return self.title

class CapturePost(models.Model):
    '''投稿されたデータを管理するモデル
    '''
    # CustomUserモデル(のuser_id)とPhotoPostモデルを
    # 1対多の関係で結び付ける
    # CustomUserが親でPhotoPostが子の関係となる
    user = models.ForeignKey(
        CustomUser,
        # フィールドのタイトル
        verbose_name='ユーザー',
        # ユーザーを削除する場合はそのユーザーの投稿データもすべて削除する
        on_delete=models.CASCADE
        )
    category = models.ForeignKey(
        Category,
        # フィールドのタイトル
        verbose_name='学年・クラス',
        # カテゴリに関連付けられた投稿データが存在する場合は
        # そのカテゴリを削除できないようにする
        on_delete=models.PROTECT
        )
    title = models.CharField(
        verbose_name='名前', # フィールドのタイトル
        max_length=200        # 最大文字数は200
        )
    # Categoryモデル(のtitle)とPhotoPostモデルを
    # 1対多の関係で結び付ける
    # Categoryが親でPhotoPostが子の関係となる
    # 名前用のフィールド
    # 学年クラスのフィールド
    num = models.CharField(
        verbose_name='種類',
        max_length=10# フィールドのタイトル        
        )
    # 英語点数用のフィールド
    score1 = models.IntegerField(
        verbose_name='英語',  # フィールドのタイトル
        )
    # 数学点数用のフィールド
    score2 = models.IntegerField(
        verbose_name='数学',  # フィールドのタイトル
        )
    # 国語点数用のフィールド
    score3 = models.IntegerField(
        verbose_name='国語',  # フィールドのタイトル
        )
    # 理科点数用のフィールド
    score4 = models.IntegerField(
        verbose_name='理科',  # フィールドのタイトル
        )
   # 社会点数用のフィールド
    score5 = models.IntegerField(
        verbose_name='社会',  # フィールドのタイトル
        )
    # 投稿日時のフィールド
    posted_at = models.DateTimeField(
        verbose_name='投稿日時', # フィールドのタイトル
        auto_now_add=True       # 日時を自動追加
        )
    
    def __str__(self):
        '''オブジェクトを文字列に変換して返す
        
        Returns(str):投稿記事のタイトル
        '''
        return self.title

