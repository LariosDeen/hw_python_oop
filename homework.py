class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = "{:.3f}".format(round(duration, 3))
        self.distance = "{:.3f}".format(round(distance, 3))
        self.speed = "{:.3f}".format(round(speed, 3))
        self.calories = "{:.3f}".format(round(calories, 3))

    def get_message(self) -> str:
        """Возвращает информационное сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.'
                )


class Training:
    """Базовый класс тренировки."""

    training_type: str = ''
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Возвращает дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Возвращает информационное сообщение
        о выполненной тренировке.
        """
        info_data = InfoMessage(self.training_type,
                                self.duration,
                                self.get_distance(),
                                self.get_mean_speed(),
                                self.get_spent_calories()
                                )
        return info_data


class Running(Training):
    """Тренировка: бег."""

    training_type: str = 'Running'
    coeff_calorie_1: int = 18
    coeff_calorie_2: int = 20

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        hour_min_change: int = 60
        duration_min = self.duration * hour_min_change
        spent_cal_min = (
            (self.coeff_calorie_1
             * self.get_mean_speed()
             - self.coeff_calorie_2) * self.weight / self.M_IN_KM
        )
        return spent_cal_min * duration_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    training_type: str = 'SportsWalking'
    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        hour_min_change: int = 60
        duration_min = self.duration * hour_min_change
        return (self.coeff_calorie_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.coeff_calorie_2 * self.weight) * duration_min


class Swimming(Training):
    """Тренировка: плавание."""

    training_type: str = 'Swimming'
    LEN_STEP: float = 1.38
    coeff_calorie_1: float = 1.1
    coeff_calorie_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость движения."""
        distance_m = self.length_pool * self.count_pool
        return distance_m / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        return (self.get_mean_speed()
                + self.coeff_calorie_1) * self.coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Считывает данные полученные от датчиков."""
    training_type = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    any_training = training_type[workout_type](*data)
    return any_training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
