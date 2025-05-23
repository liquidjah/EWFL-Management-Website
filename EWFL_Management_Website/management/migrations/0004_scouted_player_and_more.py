# Generated by Django 5.1.2 on 2024-11-06 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_alter_team_assistant_manager_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scouted_Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=64)),
                ('position', models.CharField(max_length=3)),
                ('name', models.CharField(default='Player', max_length=64)),
                ('age', models.IntegerField()),
                ('overall', models.IntegerField()),
                ('potential', models.IntegerField()),
                ('nationality', models.CharField(max_length=64)),
                ('tactic', models.CharField(max_length=64)),
                ('wage', models.IntegerField()),
                ('contract_length', models.IntegerField()),
                ('skill_points', models.IntegerField(default=0)),
                ('goals', models.IntegerField(default=0)),
                ('assists', models.IntegerField(default=0)),
                ('motm', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='team',
            old_name='wage_budget',
            new_name='wage_budget_total',
        ),
        migrations.AddField(
            model_name='team',
            name='wage_budget_remaining',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='wage_budget_spent',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='assists',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='goals',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='motm',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(default='Player', max_length=64),
        ),
        migrations.AlterField(
            model_name='player',
            name='skill_points',
            field=models.IntegerField(default=0),
        ),
    ]
