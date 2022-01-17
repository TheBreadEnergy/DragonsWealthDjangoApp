from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView
from DragonsWealth.forms import RegisterUserForm, LoginUserForm
from DragonsWealth.tinkoff import Tinkoff
from DragonsWealth.utils import DataMixin


def index(request):
    chart = ''
    chart_size = ''

    portfolio_Stock = ''
    portfolio_ETF = ''
    portfolio_Bond = ''
    portfolio_Currency = ''
    portfolio_RUB = ''
    operations = ''

    if request.user.id is not None:
        user = User.objects.get(id=request.user.id)
        if user.profile.tinkoff_token != "":
            user_tinkoff = Tinkoff(user.profile.tinkoff_token)

            chart = user_tinkoff.chart()
            chart_size = user_tinkoff.chart_size()

            portfolio_Stock = user_tinkoff.portfolio_stock()  # Получение Акций
            portfolio_ETF = user_tinkoff.portfolio_etf()  # Получение ETF
            portfolio_Bond = user_tinkoff.portfolio_bond()  # Получение Облигаций
            portfolio_Currency = user_tinkoff.portfolio_сurrency()  # Получение баланса портфеля
            portfolio_RUB = user_tinkoff.portfolio_rub()
            operations = user_tinkoff.operations()

            context = {
                'title': 'DragonsWealth',
                'portfolio_Stock': portfolio_Stock,
                'portfolio_ETF': portfolio_ETF,
                'portfolio_Bond': portfolio_Bond,
                'portfolio_Currency': portfolio_Currency,
                'portfolio_RUB': portfolio_RUB,
                'operations': operations,
                'chart': chart,
                'chart_size': chart_size
            }

            print(context['portfolio_Stock'])

    return render(request, 'DragonsWealth/index.html', {
                'title': 'DragonsWealth',
                'portfolio_Stock': portfolio_Stock,
                'portfolio_ETF': portfolio_ETF,
                'portfolio_Bond': portfolio_Bond,
                'portfolio_Currency': portfolio_Currency,
                'portfolio_RUB': portfolio_RUB,
                'operations': operations,
                'chart': chart,
                'chart_size': chart_size
            })


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'registration/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):
    logout(request)
    return redirect('home')


def show_ticker(request, ticker):
    infoTicker = ''

    if request.user.id is not None:
        user = User.objects.get(id=request.user.id)
        if user.profile.tinkoff_token != "":
            user_tinkoff = Tinkoff(user.profile.tinkoff_token)

            portfolio_Stock = user_tinkoff.portfolio_stock()  # Получение Акций
            portfolio_ETF = user_tinkoff.portfolio_etf()  # Получение ETF
            portfolio_Bond = user_tinkoff.portfolio_bond()  # Получение Облигаций

            for number in range(0, len(portfolio_Stock)):
                if portfolio_Stock[number]['ticker'] == ticker:
                    infoTicker = portfolio_Stock[number]
            for number in range(0, len(portfolio_ETF)):
                if portfolio_ETF[number]['ticker'] == ticker:
                    infoTicker = portfolio_ETF[number]
            for number in range(0, len(portfolio_Bond)):
                if portfolio_Bond[number]['ticker'] == ticker:
                    infoTicker = portfolio_Bond[number]

    print(infoTicker)
    context = {
        'title': infoTicker['name'],
        'ticker': ticker,
        'infoTicker': infoTicker
    }

    return render(request, 'DragonsWealth/ticker.html', context=context)
