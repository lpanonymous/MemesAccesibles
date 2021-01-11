from django.shortcuts import render
from album.models import Category, Photo
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView
import pyttsx3
import speech_recognition as sr

#def first_view(request):
#    return HttpResponse('Esta es mi primera vista')
#
#
#def category(request):
#    category_list = Category.objects.all()
#    context = {'object_list': category_list}
#    return render(request, 'album/category_list.html', context)
#
#
#def category_detail(request, category_id):
#    category = Category.objects.get(id=category_id)
#    context = {'object': category}
#    return render(request, 'album/category_detail.html', context)


def base(request):
    return render(request, 'base.html')

def memes_accesible(request):
    # pip install pyttsx3 pypiwin32

    # One time initialization
    engine = pyttsx3.init()

    # Set properties _before_ you add things to say
    engine.setProperty('rate', 130)  # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1

    # Queue up things to say.
    # There will be a short break between each one
    # when spoken, like a pause between sentences.
    engine.say("Bienvenido a memes accesibles.")
    engine.say("Di cuatro para escuchar el menú de opciones o di otro número de opción que conozcas.")
    engine.runAndWait()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        o = 1
        while o == 1:
            print('Elegir opción : ')
            r.adjust_for_ambient_noise(source, duration=1) 
            audio = r.listen(source)
            try:
                opcion = r.recognize_google(audio, language = 'es-ES')
                print(opcion)
                if opcion == "uno" or opcion =="1":
                    engine.say("Elegiste la opción uno.")
                    engine.runAndWait()
                    opcion2 = "escuchar"
                    while opcion2 != "adios":
                        state = 1
                        while state == 1: 
                            if opcion2 == "escuchar":
                                for categoria in Category.objects.all():
                                    engine.say(categoria.id)
                                    engine.say(categoria.name)
                                    engine.runAndWait()
                                state = 0
                        print("Di escuchar para repetir las plantillas o no digas nada para salir de la opción.")
                        engine.say("Di escuchar para repetir las plantillas o no digas nada para salir de la opción.")
                        engine.runAndWait()
                        audio2 = r.listen(source)
                        opcion2 = r.recognize_google(audio2, language = 'es-ES')
                        state=1
                    engine.say("Elige una opción.")
                    engine.runAndWait()
                    o = 1
                elif opcion == "dos" or opcion =="2":
                    engine.say("Elegiste la opción dos.")
                    engine.runAndWait() 
                    opcion2 = "hola"
                    while opcion2 != "adios":
                        state = 1
                        while state == 1:
                            print("Dime el nombre de la plantilla:")
                            engine.say("Dime el nombre de la plantilla.")
                            engine.runAndWait()
                            audio2 = r.listen(source)
                            opcion2 = r.recognize_google(audio2, language = 'en-US')
                            print("La plantilla solicitada fue:")
                            engine.say(opcion2)
                            engine.runAndWait()
                            print(opcion2)
                            for categoria in Category.objects.all():
                                if categoria.name.lower() == opcion2.lower():
                                    engine.say(categoria.description)
                                    engine.runAndWait()
                                    audio2 = r.listen(source)
                                    opcion2 = r.recognize_google(audio2, language = 'en-US')
                                    print("La plantilla solicitada fue:")
                                    engine.say(opcion2)
                                    engine.runAndWait()
                                    print(opcion2)
                                    state = 0 
                                if categoria.name.lower() != opcion2.lower():
                                    state = 1
                    engine.say("Elige una opción.")
                    engine.runAndWait()
                    o = 1
                elif opcion =="tres" or opcion == "3":
                    engine.say("Elegiste la opción tres, dime el nombre de una plantilla.")
                    print("Nombre de plantilla:")
                    engine.runAndWait() 
                    audio2 = r.listen(source)
                    opcion2 = r.recognize_google(audio2, language = 'en-US')
                    print("La plantilla solicitada fue:")
                    engine.say(opcion2)
                    engine.runAndWait()
                    print(opcion2)
                    for meme in Photo.objects.all():
                        if meme.category.name.lower() == opcion2.lower():
                            engine.say("Texto superior.")
                            engine.say(meme.toptext)
                            engine.say("Texo inferior.")
                            engine.say(meme.bottomtext)
                            engine.runAndWait()
                            engine.say("Elige una opción.")
                            engine.runAndWait()
                            o = 1
                elif opcion =="cuatro" or opcion == "4":
                    engine.say("Uno.-Nombres de plantillas.")
                    engine.say("Dos.-Detalles de una plantilla.")
                    engine.say("Tres.-Elegir una plantilla para escuchar un meme.")
                    engine.say("Cuatro.-Repetir menú de opciones.")
                    engine.say("Cero.-Salir del sistema.")
                    engine.say("Elige el número de una opción.")
                    engine.runAndWait()
                    o = 1
                elif opcion == "cero" or opcion =="0":
                    engine.say("Elegiste la opción cero, adios.")
                    print("Elegiste la opción cero, adios.")
                    engine.stop()
                    o = 0
            except:
                engine.say("Lo siento, no puedo escucharte.")
                print('Lo siento, no puedo escucharte.')
                engine.say("Elige una opción.")
                engine.runAndWait()
                o = 1


    # Program will not continue execution until
    # all speech is done talking
    return render(request, 'album/memes_accesible.html')

class CategoryListView(ListView):
    model = Category
    #template_name = 'category.html'


class CategoryDetailView(DetailView):
    model = Category


class PhotoListView(ListView):
    model = Photo


class PhotoDetailView(DetailView):
    model = Photo


class PhotoUpdate(UpdateView):
    model = Photo
    fields = '__all__'

class PhotoCreate(CreateView):
    model = Photo
    fields = '__all__'


class PhotoDelete(DeleteView):
    model = Photo
    success_url = reverse_lazy('photo-list')