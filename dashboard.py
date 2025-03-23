import math

import pygame


class Dartboard:
   def __init__(self, pos, image_path, params=None):
      """
      :param pos: Кортеж (x, y) — центр мишени в окне.
      :param image_path: Путь до изображения мишени.
      :param params: Словарь с параметрами для расчёта зон.
        Если не указан, используются следующие значения:
          • 'board_diameter': 450         - диаметр мишени в пикселях
          • 'scoring_diameter': 358       - диаметр активной зоны попадания
          • 'scoring_radius': 358/2       - радиус этой зоны (179px)
          • 'double_ring_width': 16       - ширина зоны двойного попадания
          • 'double_ring_inner': 179-16   - внутренняя граница двойного кольца (163px)
          • 'triple_ring_width': 12       - ширина зоны тройного попадания
          • 'triple_ring_inner': 102      - внутренняя граница тройного кольца
          • 'triple_ring_outer': 114      - внешняя граница тройного кольца
          • 'bullseye_radius': 30/2       - радиус bull’s eye (15px, 50 очков)
          • 'outer_bull_radius': 58/2     - радиус внешнего bull (29px, 15 очков)
      """
      if params is None:
         self.params = {
            'board_diameter': 450,  # полный диаметр доски
            'scoring_diameter': 358,  # диаметр активной зоны попадания
            'scoring_radius': 358 / 2,  # 179px
            'double_ring_width': 16,  # ширина двойного кольца
            'double_ring_inner': (358 / 2) - 16,  # 179 - 16 = 163px
            'triple_ring_width': 11,  # ширина тройного кольца
            'triple_ring_inner': 102,  # внутренняя граница тройного кольца (эстимированная)
            'triple_ring_outer': 114,  # внешняя граница тройного кольца = 120px
            'bullseye_radius': 30 / 2,  # радиус bull’s eye = 15px (50 очков)
            'outer_bull_radius': 58 / 2,  # радиус внешнего bull = 29px (15 очков)
         }
      else:
         self.params = params

      self.pos = pos  # Центр мишени
      board_diameter = int(self.params['board_diameter'])
      # Загружаем и масштабируем изображение до нужного размера
      self.image = pygame.image.load(image_path).convert_alpha()
      self.image = pygame.transform.scale(self.image, (board_diameter, board_diameter))
      self.rect = self.image.get_rect(center=self.pos)
      self.center = self.rect.center

   @staticmethod
   def get_sector(angle):
      """
      Определяет сектор в мишени по углу удара.
      Сектора мишени расположены (по часовой стрелке, начиная с верхней части) следующим образом:
        [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]
      Корректирует угол так, чтобы сектор 20 располагался точно сверху.
      """
      sectors = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]
      # Сдвинем угол: 90° соответствует верхней точке, плюс половина сектора (9°)
      adjusted_angle = (angle - 270 + 9.5) % 360
      sector_index = int(adjusted_angle // 18)
      return sectors[sector_index]

   def evaluate_hit(self, hit_pos):
      """
      Вычисляет очки попадания по координатам удара.
      Осуществляется проверка попадания в bull's eye, внешний bull, затем в сектора с учётом
      двойного (от 163px до 179px) и тройного кольца (от 110px до 120px).
      :param hit_pos: Кортеж (x, y) координат удара.
      :return: Очки попадания (целое число). Если удар вне активной зоны – 0.
      """
      dx = hit_pos[0] - self.center[0]
      dy = hit_pos[1] - self.center[1]
      d = math.hypot(dx, dy)

      # Если удар за пределами активной зоны попадания, это промах.
      if d > self.params['scoring_radius']:
         return 0

      # Проверка bull's eye (50 очков) — внутренний круг радиуса 15px.
      if d <= self.params['bullseye_radius']:
         return 50
      # Проверка внешнего bull (15 очков) — круг радиуса 29px.
      elif d <= self.params['outer_bull_radius']:
         return 15

      # Вычисляем угол удара (от 0 до 360 градусов).
      angle = math.degrees(math.atan2(dy, dx))
      angle = (angle + 360) % 360
      base_score = Dartboard.get_sector(angle)

      # Проверка попадания в тройное кольцо (от 110px до 120px)
      if self.params['triple_ring_inner'] <= d <= self.params['triple_ring_outer']:
         return base_score * 3
      # Проверка попадания в двойное кольцо (от 163px до 179px)
      elif self.params['double_ring_inner'] <= d <= self.params['scoring_radius']:
         return base_score * 2
      # Иначе попадание засчитывается как обычное (одинарный сектор)
      else:
         return base_score

   def draw(self, surface):
      """
      Отрисовывает мишень на заданной поверхности.
      """
      surface.blit(self.image, self.rect)

