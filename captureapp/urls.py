from django.urls import path
from . import views

#URLconfのURLパターンを逆引きできるようにアプリ名を登録
app_name = 'captureapp'

#URLパターンを登録するリスト
urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    
    path('post/', views.CreateCaptureView.as_view(), name='post'),
    # 投稿完了ページへのアクセスはviewsモジュールのPostSuccessViewを実行
    path('post_done/',
         views.PostSuccessView.as_view(),
         name='post_done'),
    # カテゴリ一覧ページ
    # photos/<Categorysテーブルのid値>にマッチング
    # <int:category>は辞書{category: id値(int)}としてCategoryViewに渡される
    path('photos/<int:category>',
         views.CategoryView.as_view(),
         name = 'photos_cat'
         ),
    # 詳細ページ
    # photo-detail/<Photo postsテーブルのid値>にマッチング
    # <int:pk>は辞書{pk: id値(int)}としてDetailViewに渡される
    path('photo-detail/<int:pk>',
         views.DetailView.as_view(),
         name = 'photo_detail'
         ),
    # 投稿写真の削除
    # photo/<Photo postsテーブルのid値>/delete/にマッチング
    # <int:pk>は辞書{pk: id値(int)}としてDetailViewに渡される
    path('captureapp/<int:pk>/delete/',
         views.CapDeleteView.as_view(),
         name = 'captureapp_delete'
         ),
    path(
        #お問い合わせページのURLは「contact」
        'contact/',
        #viewsモジュールのContactViewを実行
        views.ContactView.as_view(),
        #URLパターンの名前を'contact'にする
        name='contact'
        ),
]
