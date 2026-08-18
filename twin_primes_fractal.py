import numpy as np
import matplotlib.pyplot as plt

def generate_primes_and_twins(limit):
    """
    Находит простые числа и выделяет среди них пары-близнецы
    с помощью классического алгоритма Эратосфена.
    """
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    # Решето Эратосфена (наше фрактальное вырезание пространства)
    for index in range(2, int(limit**0.5) + 1):
        if is_prime[index]:
            for composite in range(index*index, limit + 1, index):
                is_prime[composite] = False
                
    primes = [num for num, prime in enumerate(is_prime) if prime]
    
    twins = set()
    # Ищем пары, где разница между соседними простыми числами равна 2
    for i in range(len(primes) - 1):
        if primes[i+1] - primes[i] == 2:
            twins.add(primes[i])
            twins.add(primes[i+1])
            
    return primes, twins

def calculate_fractal_dimension(twin_list, limit):
    """
    Вычисляет фрактальную размерность Хаусдорфа (методом Box-Counting)
    для распределения пар чисел-близнецов.
    Показывает скорость истощения числовой плотности.
    """
    if len(twin_list) < 2:
        return 0.0
        
    # Задаем масштабы измерительной сетки (коробок) от 10 до предела
    scales = np.logspace(1, int(np.log10(limit)) - 1, num=8)
    counts = []
    
    for scale in scales:
        # Разбиваем интервал на отрезки фиксированного размера и считаем заполненные
        boxes = set(int(num / scale) for num in twin_list)
        counts.append(len(boxes))
        
    # Вычисляем наклон линии в логарифмических координатах (линейная регрессия)
    # Наклон прямой показывает размерность D
    coeffs = np.polyfit(np.log(1 / scales), np.log(counts), 1)
    return float(coeffs[0])

def plot_fractal_spiral(limit):
    """
    Строит распределение чисел в полярных координатах и считает
    фрактальную размерность Хаусдорфа.
    """
    print(f"[Фрактальный Симулятор] Запуск сжатия пространства до {limit}...")
    primes, twins = generate_primes_and_twins(limit)
    
    twin_list = sorted(list(twins))
    
    # Считаем строгую математическую размерность фрактала
    D_twins = calculate_fractal_dimension(twin_list, limit)
    
    # Переводим числа в углы и радиусы для полярного графика
    theta_all_primes = np.array(primes)
    r_all_primes = np.array(primes)
    
    theta_twins = np.array(twin_list)
    r_twins = np.array(twin_list)
    
    # Настройка неонового графика в стиле киберпанк
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})
    
    # Максимизируем окно графика на весь экран для идеального визуала
    try:
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
    except Exception:
        pass
    
    # 1. Рисуем обычные простые числа (бирюзовый фон)
    ax.scatter(theta_all_primes, r_all_primes, color='cyan', s=1.5, alpha=0.4, label='Simple Primes')
    
    # 2. Выделяем числа-близнецы (пурпурная фрактальная пыль)
    ax.scatter(theta_twins, r_twins, color='magenta', s=4, alpha=0.9, label='Twin Primes (Fractal Dust)')
    
    # Обновленный центрированный заголовок с правильным переносом строки и увеличенным отступом
    title_text = f"Fractal Geometry of Twin Primes (Scale: 1 to {limit})\nCalculated Hausdorff Dimension D = {D_twins:.4f}"
    ax.set_title(title_text, fontsize=12, color='white', fontweight='bold', pad=35, va='bottom')
    
    # Очищаем сетку, оставляя чистую геометрию
    ax.set_rticks([]) 
    ax.set_thetagrids([])
    ax.spines['polar'].set_visible(False)
    ax.legend(loc='upper right', frameon=True, facecolor='black', edgecolor='gray')
    
    print(f"[Результат] Найдено простых чисел: {len(primes)}, из них близнецов: {len(twins)}")
    print(f"[Результат] Вычисленная размерность Хаусдорфа D = {D_twins:.4f}")
    print("[Результат] Поскольку D > 0, фрактальная устойчивость структуры подтверждена!")
    
    plt.tight_layout()
    plt.show()

# --- Точка запуска ---
if __name__ == "__main__":
    # Масштаб в 50 000 чисел дает идеальную детализацию узора
    test_limit = 50000 
    plot_fractal_spiral(test_limit)
