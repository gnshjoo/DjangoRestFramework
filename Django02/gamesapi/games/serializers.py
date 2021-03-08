from rest_framewrok import serializers
from games.models import GameCategory
from games.models import Game
from games.models import Player
from games.models import PlayerScore


class GameCategorySerializer(serializers.HyperlinkedModelSerializer):
    games = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='game-detail'
    )

    class Meta:
        model = GameCategory
        fields = (
            'url',
            'pk',
            'name',
            'games',
        )

class GameSeializer(serializers.HyperlinkedModelSerializer):
    game_category = serializers.SlugRelatedField(
        queryset=GameCategory.objects.all(), slug_field='name'
    )

    class Meta:
        model = Game
        field = (
            'url',
            'game_category',
            'name',
            'release_date',
            'played'
        )

class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    game = GameSeializer()

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'game',
        )

class PlayerSerializer(serializers.HyperlinkedModelSerializer):

    scores = ScoreSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(
        choice=Player.GENDER_CHOICES
    )
    gender_description = serializers.ChoiceField(
        source='get_gender_display',
        read_only=True
    )

    class Meta:
        model = Player
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'scores',
        )

class PlayerScoreSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(queryset=Player.objects.all(), slug_field='name')
    game = serializers.SlugRelatedField(queryset=Game.objects.all(), slug_field='name')

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_data',
            'player',
            'game',
        )
