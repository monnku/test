import pygame
import sys
import random

# 初期化
pygame.init()

# 画面サイズ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("シューティングゲーム")

# 色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# プレイヤー
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - 2 * player_size
player_speed = 5
player_life = 3

# 弾
bullet_size = 10
bullet_speed = 7
bullet_reload_time = 200  # ミリ秒
last_bullet_time = pygame.time.get_ticks()
bullets = []

# 敵
enemy_size = 50
enemy_speed = 3
enemy_spawn_frequency = 0.02  # 1秒あたりの敵の出現確率
enemies = []

# 背景
background = pygame.image.load("space_background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# スコア
score = 0

# フォント
font = pygame.font.Font(None, 36)

# ゲームオーバー画面のフォント
game_over_font = pygame.font.Font(None, 72)

# クリア画面のフォント
clear_font = pygame.font.Font(None, 72)

# ゲームの状態
game_state = "playing"

# ゲームループ
clock = pygame.time.Clock()
game_running = True

while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # ゲームオーバーまたはクリアの場合、キー入力でゲームを再開
    keys = pygame.key.get_pressed()
    if game_state != "playing" and keys[pygame.K_RETURN]:
        # ゲームの初期化
        player_x = WIDTH // 2 - player_size // 2
        player_y = HEIGHT - 2 * player_size
        player_life = 3
        bullets = []
        enemies = []
        score = 0
        game_state = "playing"

    if game_state == "playing":
        # プレイヤーの移動
        if keys[pygame.K_LEFT] and player_x - player_speed > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_size + player_speed < WIDTH:
            player_x += player_speed

        # 弾の発射
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - last_bullet_time > bullet_reload_time:
            bullet = pygame.Rect(player_x + player_size // 2 - bullet_size // 2, player_y, bullet_size, bullet_size)
            bullets.append(bullet)
            last_bullet_time = current_time

        # 弾の移動
        for bullet in bullets:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # 敵の生成
        if random.random() < enemy_spawn_frequency:
            enemy = pygame.Rect(random.randint(0, WIDTH - enemy_size), 0, enemy_size, enemy_size)
            enemies.append(enemy)

        # 敵の移動
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                player_life -= 1

        # 衝突判定
        for bullet in bullets:
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1

        # プレイヤーと敵の衝突判定
        for enemy in enemies:
            if enemy.colliderect(pygame.Rect(player_x, player_y, player_size, player_size)):
                enemies.remove(enemy)
                player_life -= 1

        # ゲームオーバー判定
        if player_life <= 0:
            game_state = "game_over"

        # クリア判定（敵を一定数倒した場合）
        if score >= 20:
            game_state = "clear"

    # 画面の描画
    screen.blit(background, (0, 0))

    if game_state == "playing":
        # プレイヤーの描画
        pygame.draw.rect(screen, RED, (player_x, player_y, player_size, player_size))

        # 弾の描画
        for bullet in bullets:
            pygame.draw.rect(screen, RED, bullet)

        # 敵の描画
        for enemy in enemies:
            pygame.draw.rect(screen, BLUE, enemy)

        # スコアの表示
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (10, 10))

        # ライフの表示
        life_text = font.render(f"Life: {player_life}", True, RED)
        screen.blit(life_text, (WIDTH - 100, 10))

    elif game_state == "game_over":
        # ゲームオーバー画面の表示
        game_over_text = game_over_font.render("Game Over", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        instruction_text = font.render("Press Enter to restart", True, RED)
        screen.blit(instruction_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))

    elif game_state == "clear":
        # クリア画面の表示
        clear_text = clear_font.render("Congratulations! You Win!", True, RED)
        screen.blit(clear_text, (WIDTH // 2 - 300, HEIGHT // 2 - 50))
        instruction_text = font.render("Press Enter to restart", True, RED)
        screen.blit(instruction_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
