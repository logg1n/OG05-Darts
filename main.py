import pygame
import sys

from dashboard import Dartboard

def main():
   FPS = 60
   WIDTH, HEIGHT = 600, 600

   pygame.init()
   screen = pygame.display.set_mode((WIDTH, HEIGHT))
   pygame.display.set_caption("Dartboard Demo")
   # Загрузка изображения фона
   background = pygame.image.load("image/background.jpg").convert()
   # Если размер фона отличается от размера окна, можно его масштабировать:
   background = pygame.transform.scale(background, (WIDTH, HEIGHT))

   # Настройка шрифтов для отображения очков
   font = pygame.font.Font(None, 36)

   pygame.mouse.set_visible(0)

   clock = pygame.time.Clock()

   # Создаем объект мишени в центре экрана; файл "dartboard.png" должен быть в рабочей директории.
   dartboard = Dartboard(pos=(WIDTH // 2, HEIGHT // 2), image_path="image/target.png")

   # Переменные для подсчёта очков и бросков
   total_score = 0
   round_score = 0
   throws = 0
   max_throws = 3  # Броски до сброса

   running = True
   while running:
      clock.tick(FPS)

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False
         elif event.type == pygame.MOUSEBUTTONDOWN:
            hit = event.pos
            score = dartboard.evaluate_hit(hit)
            total_score += score
            throws += 1
            print(f"Попадание в точке {hit} → Очки: {score}")

            # Проверяем количество бросков
            if throws >= max_throws:
               print(f"Всего очков за раунд: {total_score}")
               round_score = total_score
               total_score = 0  # Сбрасываем счёт
               throws = 0  # Сбрасываем броски

      # Отрисовываем фон
      screen.blit(background, (0, 0))

      # Отрисовка мишени
      dartboard.draw(screen)

      mouse_pos = pygame.mouse.get_pos()
      pygame.draw.circle(screen, pygame.Color("blue"), mouse_pos, 3)

      # Отображаем счёт в верхней части экрана
      score_text = font.render(f"Очки: {total_score} | Броски: {throws}/{max_throws}", True, (255, 215, 0))
      screen.blit(score_text, (10, 10))

      round_text = font.render(f"Очки: {round_score}", True, (255, 215, 0))
      screen.blit(round_text, (WIDTH - 150, 10))

      pygame.display.flip()

   pygame.quit()
   sys.exit()


if __name__ == "__main__":
   main()
