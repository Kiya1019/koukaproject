from django.shortcuts import render

from django.views.generic import TemplateView, ListView

# django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
# formsモジュールからPhotoPostFormをインポート
from .forms import CapturePostFrom
# method_decoratorをインポート
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required
from .models import CapturePost
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.views.generic import FormView
# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy
#fromsモジュールからContactFormをインポート
from .forms import ContactForm
#django.contribからmesseageをインポート
from django.contrib import messages
#django.core.mailモジュールからEmailMessageをインポート
from django.core.mail import EmailMessage


class IndexView(ListView):
    #index.htmlをレンダリングする
    template_name = 'index.html'
    queryset = CapturePost.objects.order_by('-posted_at')
    paginate_by=9
class CreateCaptureView(CreateView):
    '''写真投稿ページのビュー
    
    PhotoPostFormで定義されているモデルとフィールドと連携して
    投稿データをデータベースに登録する
    
    Attributes:
      form_class: モデルとフィールドが登録されたフォームクラス
      template_name: レンダリングするテンプレート
      success_url: データベスへの登録完了後のリダイレクト先
    '''
    # forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class = CapturePostFrom
    # レンダリングするテンプレート
    template_name = "post_cap.html"
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('captureapp:post_done')

    def form_valid(self, form):
        '''CreateViewクラスのform_valid()をオーバーライド
        
        フォームのバリデーションを通過したときに呼ばれる
        フォームデータの登録をここで行う
        
        parameters:
          form(django.forms.Form):
            form_classに格納されているPhotoPostFormオブジェクト
        Return:
          HttpResponseRedirectオブジェクト:
            スーパークラスのform_valid()の戻り値を返すことで、
            success_urlで設定されているURLにリダイレクトさせる
        '''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー
    
    Attributes:
      template_name: レンダリングするテンプレート
    '''
    # index.htmlをレンダリングする
    template_name ='post_success.html'
class DetailView(DetailView):
    '''詳細ページのビュー
    
    投稿記事の詳細を表示するのでDetailViewを継承する
     Attributes:
      template_name: レンダリングするテンプレート
      model: モデルのクラス
    '''
    # post.htmlをレンダリングする
    template_name ='detail.html'
    # クラス変数modelにモデルBlogPostを設定
    model = CapturePost
class CategoryView(ListView):
    '''カテゴリページのビュー
    
    Attributes:
      template_name: レンダリングするテンプレート
      paginate_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name ='index.html'
    # 1ページに表示するレコードの件数
    paginate_by = 9

    def get_queryset(self):
      '''クエリを実行する
      
      self.kwargsの取得が必要なため、クラス変数querysetではなく、
      get_queryset（）のオーバーライドによりクエリを実行する
      
      Returns:
        クエリによって取得されたレコード
      '''     
      # self.kwargsでキーワードの辞書を取得し、
      # categoryキーの値(Categorysテーブルのid)を取得
      category_id = self.kwargs['category']
      # filter(フィールド名=id)で絞り込む
      categories = CapturePost.objects.filter(
        category=category_id).order_by('-posted_at')
      # クエリによって取得されたレコードを返す
      return categories
class CapDeleteView(DeleteView):
    '''レコードの削除を行うビュー
    
    Attributes:
      model: モデル
      template_name: レンダリングするテンプレート
      paginate_by: 1ページに表示するレコードの件数
      success_url: 削除完了後のリダイレクト先のURL
    '''
    # 操作の対象はPhotoPostモデル
    model = CapturePost
    # photo_delete.htmlをレンダリングする
    template_name ='captureapp_delete.html'
    # 処理完了後にマイページにリダイレクト
    success_url = reverse_lazy('captureapp:index')

    def delete(self, request, *args, **kwargs):
      '''レコードの削除を行う
      
      Parameters:
        self: PhotoDeleteViewオブジェクト
        request: WSGIRequest(HttpRequest)オブジェクト
        args: 引数として渡される辞書(dict)
        kwargs: キーワード付きの辞書(dict)
                {'pk': 21}のようにレコードのidが渡される
      
      Returns:
        HttpResponseRedirect(success_url)を返して
        success_urlにリダイレクト
      '''
      # スーパークラスのdelete()を実行
      return super().delete(request, *args, **kwargs)
class ContactView(FormView):
    '''問い合わせページを表示するビュー
    
    フォームで入力されたデータを取得しメール作成と送信を行う
    '''
    #contact.htmlをレンダリングする
    template_name ='contact.html'
    #クラス変数form_classにforms.pyで定義したContactFormを設定
    form_class= ContactForm
    #送信完了後にリダイレクトするページ
    success_url=reverse_lazy('captureapp:contact')
    
    def form_valid(self, form):
        '''FormViewクラスのForm_valid()をオーバーライド
        
        フォームのバリデーションを通過したデータがPOSTされた時に呼ばれる
        メール送信を行う
        
        parameters:
          form(object): ContactFormのオブジェクト
        Return:
          HttpResponseReddirectのオブジェクト
          オブジェクトをインスタンス化するとsuccess_urlで
          設定されるURLにリダイレクトされる
        '''
        #フォームに入力されたデータをフィールド名を指定して取得
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        #メールのタイトルの書式設定
        subject = 'お問い合わせ:{}'.format(title)
        #フォームの入力データの書式設定
        message = \
            '送信者名:{0}\nメールアドレス:{1}\n タイトル:{2}\n メッセージ:\n{3}'\
                .format(name, email, title, message)
        #メールの送信元のアドレス
        from_email = 'mcd2376076@stu.o-hara.ac.jp'
        #メールの送信先のアドレス
        to_list = ['mcd2376076@stu.o-hara.ac.jp']
        #EmailMessageオブジェクトを生成
        message = EmailMessage(subject=subject,
                               body=message,
                               from_email=from_email,
                               to=to_list,
                               )
        #EmailMEssageクラスのsend()でメールサーバーからメール送信
        message.send()
        #送信完了後に表示するメッセージ
        messages.success(self.request,'お問い合わせは正常に送信されました。')
        #戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)