import pygame
import random
import math

pygame.init()

class GUI:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE
    BUTTON_BG_COLOR = (230, 230, 230)
    BUTTON_HOVER_COLOR = (200, 200, 200)

    GRADIENTS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    BUTTON_FONT = pygame.font.SysFont('comicsans', 20)

    SIDE_PADDING = 100
    TOP_PADDING = 150

    def __init__(self, screen_width, screen_height, initial_values):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.window = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_values(initial_values)

        self.algorithm_options = ["Bubble Sort", "Insertion Sort"]
        self.selected_algorithm = self.algorithm_options[0]
        self.dropdown_active = False
        self.dropdown_rect = pygame.Rect(50, 100, 200, 30)
        self.button_reset = pygame.Rect(300, 100, 100, 30)
        self.button_start = pygame.Rect(450, 100, 100, 30)

    def set_values(self, values_list):
        self.values_list = values_list
        self.min_value = min(values_list)
        self.max_value = max(values_list)

        self.block_width = round((self.screen_width - self.SIDE_PADDING) / len(values_list))
        self.block_height = math.floor((self.screen_height - self.TOP_PADDING) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PADDING // 2

    def draw_interface(self, is_ascending):
        self.window.fill(self.BACKGROUND_COLOR)

        title_text = f"{self.selected_algorithm} - {'Ascending' if is_ascending else 'Descending'}"
        title = self.LARGE_FONT.render(title_text, 1, self.GREEN)
        self.window.blit(title, (self.screen_width / 2 - title.get_width() / 2, 5))

        self.draw_dropdown()

        self.draw_button(self.button_reset, "Reset", self.BUTTON_FONT)
        self.draw_button(self.button_start, "Start", self.BUTTON_FONT)

        self.draw_values()
        pygame.display.update()

    def draw_button(self, button_rect, text, font):
        pygame.draw.rect(self.window, self.BUTTON_BG_COLOR, button_rect)
        pygame.draw.rect(self.window, self.BLACK, button_rect, 2)
        text_surface = font.render(text, 1, self.BLACK)
        text_x = button_rect.x + (button_rect.width - text_surface.get_width()) // 2
        text_y = button_rect.y + (button_rect.height - text_surface.get_height()) // 2
        self.window.blit(text_surface, (text_x, text_y))

    def draw_dropdown(self):
        pygame.draw.rect(self.window, self.BUTTON_BG_COLOR, self.dropdown_rect)
        pygame.draw.rect(self.window, self.BLACK, self.dropdown_rect, 2)
        dropdown_text = self.FONT.render(self.selected_algorithm, 1, self.BLACK)
        dropdown_text_x = self.dropdown_rect.x + 10  # Adjust text padding inside the button
        dropdown_text_y = self.dropdown_rect.y + (self.dropdown_rect.height - dropdown_text.get_height()) // 2
        self.window.blit(dropdown_text, (dropdown_text_x, dropdown_text_y))

        if self.dropdown_active:
            for i, option in enumerate(self.algorithm_options):
                option_rect = pygame.Rect(self.dropdown_rect.x, self.dropdown_rect.y + (i + 1) * 30, self.dropdown_rect.width, 30)

                pygame.draw.rect(self.window, self.BUTTON_BG_COLOR, option_rect)
                pygame.draw.rect(self.window, self.BLACK, option_rect, 2)

                option_text = self.FONT.render(option, 1, self.BLACK)
                option_text_x = option_rect.x + 10
                option_text_y = option_rect.y + (option_rect.height - option_text.get_height()) // 2

                self.window.blit(option_text, (option_text_x, option_text_y))

    def draw_values(self, highlighted_positions=None, clear_background=False):
        highlighted_positions = highlighted_positions or {}
        values_list = self.values_list

        if clear_background:
            clear_rect = (
                self.SIDE_PADDING // 2,
                self.TOP_PADDING,
                self.screen_width - self.SIDE_PADDING,
                self.screen_height - self.TOP_PADDING
            )
            pygame.draw.rect(self.window, self.BACKGROUND_COLOR, clear_rect)

        for index, value in enumerate(values_list):
            x_position = self.start_x + index * self.block_width
            y_position = self.screen_height - (value - self.min_value) * self.block_height

            color = self.GRADIENTS[index % 3]

            if index in highlighted_positions:
                color = highlighted_positions[index]

            pygame.draw.rect(self.window, color, (x_position, y_position, self.block_width, self.screen_height))

        if clear_background:
            pygame.display.update()

class SortingAlgorithm:
    @staticmethod
    def bubble_sort(gui, ascending=True):
        values_list = gui.values_list

        for i in range(len(values_list) - 1):
            for j in range(len(values_list) - 1 - i):
                current_value = values_list[j]
                next_value = values_list[j + 1]

                if (current_value > next_value and ascending) or (current_value < next_value and not ascending):
                    values_list[j], values_list[j + 1] = next_value, current_value
                    gui.draw_values({j: gui.GREEN, j + 1: gui.RED}, True)
                    yield True

        return values_list

    @staticmethod
    def insertion_sort(gui, ascending=True):
        values_list = gui.values_list

        for i in range(1, len(values_list)):
            current_value = values_list[i]

            while True:
                is_ascending = i > 0 and values_list[i - 1] > current_value and ascending
                is_descending = i > 0 and values_list[i - 1] < current_value and not ascending

                if not is_ascending and not is_descending:
                    break

                values_list[i] = values_list[i - 1]
                i -= 1
                values_list[i] = current_value
                gui.draw_values({i - 1: gui.GREEN, i: gui.RED}, True)
                yield True

        return values_list

    @staticmethod
    def quick_sort(gui, ascending=True):
        pass

def generate_random_list(length, min_value, max_value):
    return [random.randint(min_value, max_value) for _ in range(length)]

def main():
    is_running = True
    clock = pygame.time.Clock()

    list_length = 50
    min_value = 0
    max_value = 100

    values_list = generate_random_list(list_length, min_value, max_value)
    gui = GUI(800, 600, values_list)
    is_sorting = False
    is_ascending = True

    sorting_algorithm = SortingAlgorithm.bubble_sort
    sorting_algorithm_generator = None

    while is_running:
        clock.tick(60)

        if is_sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                is_sorting = False
        else:
            gui.draw_interface(is_ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if gui.dropdown_rect.collidepoint(mouse_x, mouse_y):
                    gui.dropdown_active = not gui.dropdown_active
                elif gui.dropdown_active:
                    for i, option in enumerate(gui.algorithm_options):
                        option_rect = pygame.Rect(50, 130 + i * 30, 200, 30)
                        if option_rect.collidepoint(mouse_x, mouse_y):
                            gui.selected_algorithm = option
                            gui.dropdown_active = False
                            if option == "Bubble Sort":
                                sorting_algorithm = SortingAlgorithm.bubble_sort
                            elif option == "Insertion Sort":
                                sorting_algorithm = SortingAlgorithm.insertion_sort

                elif gui.button_reset.collidepoint(mouse_x, mouse_y):
                    values_list = generate_random_list(list_length, min_value, max_value)
                    gui.set_values(values_list)
                    is_sorting = False

                elif gui.button_start.collidepoint(mouse_x, mouse_y) and not is_sorting:
                    is_sorting = True
                    sorting_algorithm_generator = sorting_algorithm(gui, is_ascending)

    pygame.quit()

if __name__ == "__main__":
    main()
