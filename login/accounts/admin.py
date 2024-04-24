from django.contrib import admin
from .models import Interest, Profile

# Register your models here.
admin.site.register(Interest)
admin.site.register(Profile)

"""
{% extends 'core/base.html' %}

{% block content %}

{% if request.user.is_authenticated %}
<div class="row">
    <div class="col-md-4">
        <div class="card">
            <img src={{ user.profile.image.url }} class="card-img-top" alt="...">
            <div class="card-body">
                <h3 class="card-title text-primary">{{ user.first_name }} {{ user.last_name }}</h3>
                <h5 class="card-title">@{{ user.username | upper }}</h5>
                <small><i class="bi bi-geo-alt"></i> {{ user.profile.location }}</small>
                <p class="card-text mt-3">{{ user.profile.bio }}</p>

                <strong>Intereses:</strong> <br>

                {% for interest in user.profile.interests.all %}
                    <span class="badge bg-secondary">{{ interest.name | upper }}</span>
                {% endfor %}

                <hr>
                <a href={% url 'logout' %} class="btn btn-sm btn-success">Cerrar Sesión</a>
            </div>
        </div>
    </div>
    <div class="col-md-8">
        <h4>Título cualquiera</h4>
        <p>{% lorem %}</p>
    </div>
</div>
{% else %}
    <h4>Título cualquiera</h4>
    <p>{% lorem %}</p>
{% endif %}

{% endblock %}"""