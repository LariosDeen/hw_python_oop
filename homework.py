from dataclasses import dataclass, asdict
from typing import Dict, Type, List, Tuple


@dataclass
class InfoMessage:
    """Training information message."""

    training_type: str
    duration: str
    distance: str
    speed: str
    calories: str
    MESSAGE_TEMPLATE: str = ('Тип тренировки: {training_type}; '
                             'Длительность: {duration} ч.; '
                             'Дистанция: {distance} км; '
                             'Ср. скорость: {speed} км/ч; '
                             'Потрачено ккал: {calories}.'
                             )

    def get_message(self) -> str:
        """Returns information message about the training."""
        return self.MESSAGE_TEMPLATE.format(**asdict(self))


class Training:
    """Basic training class."""

    HOUR_MIN_CHANGE: int = 60
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Returns distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Returns the average movement speed."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Returns the number of spent calories."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Returns an information message about completed training"""
        info_data: InfoMessage = InfoMessage(self.__class__.__name__,
                                             f'{self.duration:.3f}',
                                             f'{self.get_distance():.3f}',
                                             f'{self.get_mean_speed():.3f}',
                                             f'{self.get_spent_calories():.3f}'
                                             )
        return info_data


class Running(Training):
    """Training: run."""

    RUNNING_CALORIES_MULTIPLIER: int = 18
    RUNNING_CALORIES_DIMINUTION: int = 20

    def get_spent_calories(self) -> float:
        """Returns the number of spent calories."""
        duration_min: float = self.duration * self.HOUR_MIN_CHANGE
        spent_cal_min: float = (
            (self.RUNNING_CALORIES_MULTIPLIER
             * self.get_mean_speed()
             - self.RUNNING_CALORIES_DIMINUTION)
            * self.weight / self.M_IN_KM
        )
        return spent_cal_min * duration_min


class SportsWalking(Training):
    """Training: race walking."""

    WALKING_WEIGHT_MULTIPLIER: float = 0.035
    WALKING_SECOND_MULTIPLIER: float = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Returns the number of spent calories."""
        duration_min: float = self.duration * self.HOUR_MIN_CHANGE
        return (self.WALKING_WEIGHT_MULTIPLIER * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.WALKING_SECOND_MULTIPLIER * self.weight) * duration_min


class Swimming(Training):
    """Training: swimming."""

    LEN_STEP: float = 1.38
    CALORIES_ADDEND: float = 1.1
    CALORIES_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Returns the average movement speed."""
        distance_m: float = self.length_pool * self.count_pool
        return distance_m / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Returns the number of spent calories."""
        return ((self.get_mean_speed()
                 + self.CALORIES_ADDEND)
                * self.CALORIES_MULTIPLIER
                * self.weight
                )


def read_package(workout_type: str, data: List[int]) -> Training:
    """Reads data received from sensors."""
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
    """Main function."""
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
