from dataclasses import dataclass
from typing import Dict, Type, List, Tuple


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    training_type_text: str = 'Тип тренировки'
    duration_text: str = 'Длительность'
    distance_text: str = 'Дистанция'
    mean_speed_text: str = 'Ср. скорость'
    spent_calories_text: str = 'Потрачено ккал'
    hour_text: str = 'ч.'
    km_text: str = 'км'
    km_hour_text: str = 'км/ч'

    def get_message(self) -> str:
        """Возвращает информационное сообщение о тренировке."""
        return (f'{self.training_type_text}: {self.training_type}; '
                f'{self.duration_text}: {self.duration:.3f} '
                f'{self.hour_text}; '
                f'{self.distance_text}: {self.distance:.3f} '
                f'{self.km_text}; '
                f'{self.mean_speed_text}: {self.speed:.3f} '
                f'{self.km_hour_text}; '
                f'{self.spent_calories_text}: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    hour_min_change: int = 60
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

    def __str__(self) -> str:
        return f'{self.__class__.__name__}'

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
        info_data: InfoMessage = InfoMessage(self.__str__(),
                                             self.duration,
                                             self.get_distance(),
                                             self.get_mean_speed(),
                                             self.get_spent_calories()
                                             )
        return info_data


class Running(Training):
    """Тренировка: бег."""

    running_calories_multiplier: int = 18
    running_calories_diminution: int = 20

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        duration_min: float = self.duration * self.hour_min_change
        spent_cal_min: float = (
            (self.running_calories_multiplier
             * self.get_mean_speed()
             - self.running_calories_diminution)
            * self.weight / self.M_IN_KM
        )
        return spent_cal_min * duration_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    walking_weight_multiplier: float = 0.035
    walking_second_multiplier: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        duration_min = self.duration * self.hour_min_change
        return (self.walking_weight_multiplier * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.walking_second_multiplier * self.weight) * duration_min


class Swimming(Training):
    """Тренировка: плавание."""

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
        distance_m: float = self.length_pool * self.count_pool
        return distance_m / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий."""
        return (self.get_mean_speed()
                + self.coeff_calorie_1) * self.coeff_calorie_2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Считывает данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        any_training: Training = training_type[workout_type](*data)
    except KeyError:
        print('Unknown training type')
    except TypeError:
        print('Unknown training data')
    else:
        return any_training


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
