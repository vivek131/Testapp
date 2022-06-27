from django.shortcuts import render
from OTS.models import Question,User
from django.http import HttpResponseRedirect,HttpResponse
import random
 #for random question
# Create your views here.
def newQuestion(request):#yha qestion sirh form mai likha jaega
    try:
        if request.session['username'] ==  'admin':
            pass
        else:
            return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/home/")
    except:
         return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/login/")

    res=render(request,'OTS/new_question.html')#template k andar ka OTS hai
    return res

def saveQuestion(request):#ye question ko database mai insert krdega
    #jo bhi form k dwara aaega use hum request se access krenge in short user se data le rhe hai
    question=Question()#class or table from models.py
    question.que=request.POST['question']#post is dictionary and we get keys from html form which is nothing but name attribute
    question.optiona=request.POST['optiona']
    question.optionb=request.POST['optionb']
    question.optionc=request.POST['optionc']
    question.optiond=request.POST['optiond']
    question.answer=request.POST['answer']
    question.save()#every model class object has a method called save
    return HttpResponseRedirect('https://testpariksha.herokuapp.com/OTS/view-questions/')
     #in views we return something so here we are redirecting the questionframer(user) to the page where he can view all questions after filling one question

def viewQuestions(request):
     try:
        if request.session['username'] == 'admin':
            pass
        else:
            return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/home/")
     except:
         return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/login/")
     questions=Question.objects.all()#Question is class aur ojects jo hai uske parent class mai hai, to all likhne se vo saare objects ko represent krne lga hai
     #ab hum question ami saare data agya hai jo bhi model yaani database mai hai
     res=render(request,'OTS/view_questions.html',{'questions':questions})#template k andar ka OTS hai
     return res

def viewusers(request):
    try:
        if request.session['username']=='admin':
            pass
        else:
            return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/home/")
    except:
         return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/login/")
    users=User.objects.all()
    res=render(request,'OTS/view_user.html',{'users':users})
    return res

def editQuestion(request):
    try:
        if request.session['username'] == 'admin':
            pass
        else:
            return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/home/")
    except:
         return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/login/")
    q=request.GET['qno']#link se jo bhi data ata hai use GET[] se access krte hai usme key daalkar, aur jo form se ata hai use POST se
    question=Question.objects.get(qno=int(q))
     #Question is our table jiske pass ek method objects hai jo ki saare objects ko represent kr rha hai but usme se hume ek object chahie to get( lagakar)use qno ko fetch karlo
    res=render(request,'OTS/edit_question.html',{'question':question})
    return res

def editSaveQuestion(request):
    question=Question()
    question.qno=request.POST['qno']#post k andar wala qno name hai jisse hum input k andar rkhe data ko acces krte hai
    #agar koi data already table mai present hai ,aur hum phirse same qno bheejenge to vo purane data ko ovwerite krdega
    #nhi to naye question bhejne pr nya question automatic generate hoga
    question.que=request.POST['question']
    question.optiona=request.POST['optiona']
    question.optionb=request.POST['optionb']
    question.optionc=request.POST['optionc']
    question.optiond=request.POST['optiond']
    question.answer=request.POST['answer']
    question.save()
    return HttpResponseRedirect('https://testpariksha.herokuapp.com/OTS/view-questions/')

def deleteQuestion(request):
    q=request.GET['qno']
    question=Question.objects.filter(qno=int(q))
    question.delete()
    return HttpResponseRedirect('https://testpariksha.herokuapp.com/OTS/view-questions/')

def deleteUser(request):
    u=request.GET['username']
    user=User.objects.filter(username=u)
    user.delete()
    return HttpResponseRedirect('https://testpariksha.herokuapp.com/OTS/view-users/')



def signup(request):#username exist krne pr signup par vapas aaenge with data error=1
    d1={}
    try:  #try used bcz dictionary pass to krna hi hai bt usme kuch hona bhi chahie varna key error aaegi 
        if request.GET['error']==str(1):
            d1['errmsg']='Username already taken'
    except:
        d1['errmsg']=''

    res=render(request,'OTS/signup.html',d1)
    return res
def saveUser(request):
    user=User()
    u=User.objects.filter(username=request.POST['username'])#ye user collumn mai check krne k le ki khin username already exist to nhi krta
    if not u: #agar nhi mila to
        user.username=request.POST['username']
        user.password=request.POST['password']
        user.realname=request.POST['realname']
        user.save()
        url="https://testpariksha.herokuapp.com/OTS/login" #agar new user hai to go to login page

    else:
        url="https://testpariksha.herokuapp.com/OTS/signup/?error=1" #nhi to use signup page pr hi roko

    return HttpResponseRedirect(url)

def createAdmin():
    user=User()
    user.username="admin"
    user.password="password"
    user.realname="Superuser"
    user.save()


def login(request):
    user=User.objects.filter(username="admin")#ye check krga ek baari ki admin hai ya nhi
    if not user:       #agar nhi hua to createAdmin() ko call krke bnalo
        createAdmin()
    res=render(request,'OTS/login.html')
    return res

def loginValidation(request):
    try:
        user=User.objects.get(username=request.POST['username'],password=request.POST['password'])
        user.username    #ye exception raise karega agar username nhi hua to
        request.session['username']=user.username
        request.session['realname']=user.realname#session variables
        url="https://testpariksha.herokuapp.com/OTS/home/"#exception na hone par hum home par jaenge
    except:
        url="https://testpariksha.herokuapp.com/OTS/login/"#hone par usi form mai reh jaenge

    return HttpResponseRedirect(url)#ye page pr redirect krne k lie
def logout(request):
    request.session.clear()#destroy the session variable
    url="https://testpariksha.herokuapp.com/OTS/login/"
    return HttpResponseRedirect(url)

def home(request):
    try:
        realname=request.session['realname']#agar bina login kie hi home par jaane ki kosis krega to session variable bna hi nhi hoga to keyerror aajaegi
    except KeyError:
        return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/login/")

    res=render(request,'OTS/home.html')
    return res
def startTest(request):
     try:
        if request.session['username'] == 'admin':
            return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/home/")
        else:
            pass
     except:
         return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/login/")
     no_of_questions=5
     question_pool=list(Question.objects.all())#Question.objects.all se saare question aajenge jise hum list mai convert renge
     random.shuffle(question_pool) #us list ko har baar shuufle krenge(shuffling of question)
     questions_list=question_pool[:no_of_questions]#slicing used start from 0 to 4
     res=render(request,'OTS/start_test.html',{'questions':questions_list})
     return res
def testResult(request):
      try:
        if request.session['username'] == 'admin':
            return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/home/")
        else:
            pass
      except:
         return HttpResponseRedirect("https://testpariksha.herokuapp.com/OTS/login/")
    #start_test.html se qno hidden form mai aur correct option aarha hai
      total_attempt=0
      total_right=0
      total_wrong=0
      qno_list=[]
    #START_TEST.Html se question number hidden form mai aur selected option aarha hai hai bs
      for k in request.POST:#POST ek dictionary hai jahan k key ka role play krega yaani start_html ka name
        if k.startswith("qno"):
            qno_list.append(int(request.POST[k]))
            #key==name(html) and value(html)==value of key
      for n in qno_list:
        question=Question.objects.get(qno=n)#vo ek particular question fetch hogya hai jo humare question paper mai tha
        try: #ho skta hai usne attempt hi na kia ho to key bani nhi hogi to error aaegi
            if(question.answer==request.POST['q'+str(n)]):#can give exception
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:
            pass
      d={
        'total_attempt':total_attempt,
        'total_right':total_right,
        'total_wrong':total_wrong,
    }
      res=render(request,'OTS/test_result.html/',d)
      return res






      




      
 
    



