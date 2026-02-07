from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from core.models import Company, Area, Activity


class Command(BaseCommand):
    help = "Crea el grupo CRUD y le asigna permisos para Company, Area y Activity"

    def add_arguments(self, parser):
        parser.add_argument(
            "--group",
            type=str,
            default="owner_company",
            help="Nombre del grupo a crear/actualizar (default: owner_company)",
        )

    def handle(self, *args, **options):
        group_name = options["group"]

        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Grupo creado: {group_name}"))
        else:
            self.stdout.write(self.style.WARNING(f"Grupo ya existía: {group_name}"))

        models = [Company, Area, Activity]
        codenames = ("add", "change", "delete", "view")

        added_count = 0

        for model in models:
            ct = ContentType.objects.get_for_model(model)
            model_name = model._meta.model_name

            perms = Permission.objects.filter(
                content_type=ct,
                codename__in=[f"{c}_{model_name}" for c in codenames],
            )

            # Asignar permisos al grupo
            for p in perms:
                group.permissions.add(p)
                added_count += 1

            self.stdout.write(
                f"Permisos asignados para {model.__name__}: "
                + ", ".join([p.codename for p in perms])
            )

        self.stdout.write(self.style.SUCCESS(f"Listo. Total permisos agregados: {added_count}"))
