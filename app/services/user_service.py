from app.models.user import User

# Classe para calcular calorias e agua
class UserService:
    @staticmethod
    def calculate_calories(user: User):
        # Calcular calorias baseado na idade, peso, altura e sexo
        if user.gender == 'male':
            bmr = 66.5 + (13.75 * user.weight) + (5.003 * user.height) - (6.75 * user.age)  
        else:
            bmr = 655 + (9.563 * user.weight) + (1.850 * user.height) - (4.676 * user.age)
        
        # Calcular calorias baseado no objetivo
        if user.goal == 'lose weight':
            calories = bmr - 500
        elif user.goal == 'maintain weight':
            calories = bmr
        elif user.goal == 'gain weight':
            calories = bmr + 500
        else:
            calories = bmr

        # Arredondar para o valor inteiro mais próximo ou com uma casa decimal
        return round(calories, 1)  

    # Calcular quantidade de agua
    @staticmethod
    def calculate_water(user: User):
        water = user.weight * 30
        
        # Arredondar para o valor inteiro mais próximo ou com uma casa decimal
        return round(water, 1)
