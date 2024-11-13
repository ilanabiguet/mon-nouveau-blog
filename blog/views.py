import random
from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Equipement
from .models import Character

def post_list(request):
        characters = Character.objects.all().order_by('team')
        equipments = Equipement.objects.all().order_by('id_equip')
        return render(request, 'blog/post_list.html', {
        'characters': characters,
        'equipments': equipments,
    })


def character_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    message = None

    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)

        if form.is_valid():
            nouveau_lieu = get_object_or_404(Equipement, id_equip=form.cleaned_data['lieu'].id_equip)

            # Vérifications des conditions liées à l'état et au lieu
            if character.etat in ['affamé', 'assoiffé', 'fatigué']:
                if nouveau_lieu.id_equip in ['Practice', 'Putting green', 'Parcours de golf']:
                    message = f"{character.id_character} est {character.etat}, il ne peut pas aller ici."
                    return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

            if character.etat == 'endormi' and nouveau_lieu.id_equip != 'Hôtel':
                character.etat = "réveillé"
                character.save()
                message = f"{character.id_character} est réveillé mais il a besoin de temps pour se lever : redemandez le changement de lieu"
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

            if character.etat == 'hydraté' and nouveau_lieu.id_equip == 'Fontaine à eau':
                message = f"{character.id_character} est déjà hydraté, il ne veut pas aller à la fontaine à eau."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

            if character.etat == 'repus' and nouveau_lieu.id_equip == 'Restaurant':
                message = f"{character.id_character} est repus, il ne veut pas aller au restaurant."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

            # Vérifier si le lieu choisi est déjà occupé
            if nouveau_lieu.id_equip == 'Fontaine à eau'and nouveau_lieu.disponibilite == "occupé":
                message = f"Le lieu {nouveau_lieu.id_equip} est déjà occupé. Choisissez un autre lieu."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

          
            ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()

         
            form.save()

            # J'ai considéré qu'il n'y avait que la fontaine à eau qui nécessitait d'être notée comme libre ou occupée les autres endroits sont tout le temps libres
            if nouveau_lieu.id_equip == "Fontaine à eau":
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
            else :
                nouveau_lieu.disponibilite = "libre"
                nouveau_lieu.save()

            if nouveau_lieu.id_equip == "Fontaine à eau":
                character.etat = "hydraté"
                character.save()
                message = f"{character.id_character} s'est hydraté."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

            elif nouveau_lieu.id_equip == "Restaurant":
                character.etat = "repus"
                character.save()
                message = f"{character.id_character} a mangé et est repus."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

            elif nouveau_lieu.id_equip == "Hôtel":
                character.etat = "endormi"
                character.save()
                message = f"{character.id_character} va se coucher."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})
                
            elif nouveau_lieu.id_equip in ['Practice', 'Putting green', 'Parcours de golf']:
                nouveaux_etats = ["fatigué", "assoiffé", "affamé"]
                character.etat = random.choice(nouveaux_etats)
                character.save()
                message = f"{character.id_character} s'est bien rendu vers {nouveau_lieu.id_equip}."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})
        else :
            return redirect('character_detail', id_character=id_character)

    else:
        form = MoveForm(instance=character)

    return render(request, 'blog/character_detail.html', {
        'character': character,
        'form': form,
        'message': message
    })