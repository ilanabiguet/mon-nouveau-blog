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
    ancien_lieu = character.lieu  # Lieu actuel du personnage
    message = None

    if request.method == "POST":
        form = MoveForm(request.POST, instance=character)

        if form.is_valid():
            nouveau_lieu = get_object_or_404(Equipement, id_equip=form.cleaned_data['lieu'].id_equip)
           
            
            # Libérer l'ancien lieu si c'est la fontaine occupée par le personnage
            if ancien_lieu.id_equip == "Fontaine à eau" :
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()

            # Vérifications des conditions

            if character.etat == 'endormi' and nouveau_lieu.id_equip != "Hôtel":
                character.etat = "réveillé" 
                character.save()
                if nouveau_lieu.id_equip == 'Fontaine à eau':
                    if nouveau_lieu.disponibilite == "libre":
                        nouveau_lieu.disponibilite = "occupé"
                        nouveau_lieu.save()
                        character.etat = "hydraté"
                        character.lieu = nouveau_lieu  
                        character.save()
                        message = f"{character.id_character} s'est réveillé et s'est rendu à {nouveau_lieu.id_equip}."
                    else:
                        nouveau_lieu.id_equip = 'Hôtel'
                        nouveau_lieu.disponibilite = 'libre'
                        nouveau_lieu.save()
                        character.lieu = nouveau_lieu
                        character.save()
                        message = f"{character.id_character} est réveillé, mais {nouveau_lieu.id_equip} est occupé. Il reste à l'hôtel."
                else : # j'ai considéré qu'il n'y avait que la fontaine pour laquelle il était nécessaire de vérifier qu'elle était libre avant d'y aller 
                    nouveau_lieu.save()
                    character.lieu = nouveau_lieu  
                    character.save()
                    message = f"{character.id_character} s'est réveillé et s'est rendu à {nouveau_lieu.id_equip}." #son état reste éveillé donc il peut aller faire ce qu'il veut
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

            elif character.etat in ['affamé', 'assoiffé', 'fatigué'] and nouveau_lieu.id_equip in ['Practice', 'Putting green', 'Parcours de golf']:
                message = f"{character.id_character} est {character.etat}, il ne peut pas aller ici."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})
            
            elif character.etat == 'affamé' and nouveau_lieu.id_equip in ['Fontaine à eau', 'Hôtel']:
                message = f"{character.id_character} est {character.etat}, il ne peut pas aller ici."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})
            
            elif character.etat == 'assoiffé' and nouveau_lieu.id_equip in ['Restaurant', 'Hôtel']:
                message = f"{character.id_character} est {character.etat}, il ne peut pas aller ici."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})
        
            elif character.etat in ['hydraté', 'fatigué'] and nouveau_lieu.id_equip == 'Fontaine à eau':
                message = f"{character.id_character} est {character.etat}, il ne veut pas aller à la fontaine à eau."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

            elif character.etat in ['repus', 'fatigué'] and nouveau_lieu.id_equip == 'Restaurant':
                message = f"{character.id_character} est {character.etat}, il ne veut pas aller au restaurant."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})

            elif character.etat in ['repus', 'assoiffé', 'réveillé']  and nouveau_lieu.id_equip == 'Fontaine à eau' and nouveau_lieu.disponibilite == "occupé":
                message = f"La fontaine à eau est déjà occupée. {character.id_character} ne peut pas y aller pour le moment."
                return render(request, 'blog/character_detail.html', {'character': character, 'form': form, 'message': message})
            
            else :
                character.lieu = nouveau_lieu
                character.save()

            # Modifier l'état du personnage en fonction du lieu
            if nouveau_lieu.id_equip == "Fontaine à eau":
                character.etat = "hydraté"
                character.save()
                nouveau_lieu.disponibilite = "occupé"
                nouveau_lieu.save()
                message = f"{character.id_character} s'est hydraté."
            elif nouveau_lieu.id_equip == "Restaurant":
                character.etat = "repus"
                character.save()
                message = f"{character.id_character} a mangé et est repus."
            elif nouveau_lieu.id_equip == "Hôtel":
                character.etat = "endormi"
                character.save()
                message = f"{character.id_character} va se coucher."
            elif nouveau_lieu.id_equip in ['Practice', 'Putting green', 'Parcours de golf']:
                nouveaux_etats = ["fatigué", "assoiffé", "affamé"]
                character.etat = random.choice(nouveaux_etats)
                character.save()
                message = f"{character.id_character} s'est bien rendu vers {nouveau_lieu.id_equip}."

        else:
            return redirect('character_detail', id_character=id_character)

    else:
        form = MoveForm(instance=character)

    return render(request, 'blog/character_detail.html', {
        'character': character,
        'form': form,
        'message': message
    })