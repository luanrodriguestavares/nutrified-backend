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
            return bmr - 500
        
        elif user.goal == 'maintain weight':
            return bmr
        
        elif user.goal == 'gain weight':
            return bmr + 500
        
        return bmr

    # Calcular quantidade de agua
    @staticmethod
    def calculate_water(user: User):
        return user.weight * 30 