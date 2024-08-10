import os

from PIL import Image, ImageDraw, ImageFont

from dlgo.goboard_slow import GameState
from dlgo.gotypes import Player, Point


class GameVisualizer:
    def __init__(self, cell_size=30, margin=15):
        self.cell_size = cell_size
        self.margin = margin

        # Create a font object (you may need to adjust the path to a font file)
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)

    def _create_empty_board(self, num_rows, num_cols):
        image_width = 2 * self.margin + self.cell_size * (num_cols - 1)
        image_height = 2 * self.margin + self.cell_size * (num_rows - 1)
        image = Image.new("RGB", (image_width, image_height), color="bisque")
        draw = ImageDraw.Draw(image)

        # Draw the grid
        for i in range(num_cols):
            x = self.margin + i * self.cell_size
            draw.line([(x, self.margin), (x, image_height - self.margin)], fill="black")
        for i in range(num_rows):
            y = self.margin + i * self.cell_size
            draw.line([(self.margin, y), (image_width - self.margin, y)], fill="black")

        return image, draw

    def _draw_stone(self, draw, row, col, player):
        x = self.margin + col * self.cell_size
        y = self.margin + row * self.cell_size
        radius = self.cell_size // 2 - 1
        color = "black" if player == Player.black else "white"
        draw.ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            fill=color,
            outline="black",
        )

    def visualize_game(self, game_state: GameState, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        move_number = 0

        while game_state is not None:
            num_rows, num_cols = game_state.board.num_rows, game_state.board.num_cols
            image, draw = self._create_empty_board(num_rows, num_cols)

            # Draw all stones
            for row in range(num_rows):
                for col in range(num_cols):
                    point = Point(row + 1, col + 1)
                    player = game_state.board.get(point)
                    if player is not None:
                        self._draw_stone(draw, row, col, player)

            # Add move number and current player
            text = f"Move: {move_number}, Next: {game_state.next_player}"
            draw.text((10, image.height - 25), text, fill="black", font=self.font)

            # Save the image
            image.save(os.path.join(output_dir, f"move_{move_number:03d}.png"))

            # Move to the previous state
            game_state = game_state.previous_state
            move_number += 1

        print(f"Generated {move_number} images in {output_dir}")

    def visualize_game_state(self, game_state: GameState, output_path):
        num_rows, num_cols = game_state.board.num_rows, game_state.board.num_cols
        image, draw = self._create_empty_board(num_rows, num_cols)

        # Draw all stones
        for row in range(num_rows):
            for col in range(num_cols):
                point = Point(row + 1, col + 1)
                player = game_state.board.get(point)
                if player is not None:
                    self._draw_stone(draw, row, col, player)

        # Add current player
        text = f"Next: {game_state.next_player}"
        draw.text((10, image.height - 25), text, fill="black", font=self.font)

        # Save the image
        image.save(output_path)
