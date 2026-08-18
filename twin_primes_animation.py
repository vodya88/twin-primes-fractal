import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

def generate_primes_up_to(limit):
    """Быстрое базовое решето для анимации"""
    is_prime = np.ones(limit + 1, dtype=bool)
    is_prime[0:2] = False
    for i in range(2, int(np.sqrt(limit)) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = False
    primes = np.where(is_prime)[0]
    
    # Ищем близнецов
    diffs = np.diff(primes)
    twin_mask = (diffs == 2)
    left_twins = primes[:-1][twin_mask]
    right_twins = primes[1:][twin_mask]
    
    final_twins = np.empty(2 * len(left_twins), dtype=np.int64)
    final_twins[0::2] = left_twins
    final_twins[1::2] = right_twins
    return final_twins

def calculate_d_fast(twins, limit):
    """Быстрый подсчет размерности для текущего кадра"""
    if len(twins) < 5: return 0.0
    scales = np.logspace(1, int(np.log10(limit)) - 1, num=5)
    counts = []
    for scale in scales:
        boxes = np.unique((twins / scale).astype(np.int64))
        counts.append(len(boxes))
    coeffs = np.polyfit(np.log(1 / scales), np.log(counts), 1)
    return float(coeffs[0])

# --- Настройка графического движка ---
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})

# Задаем шаги анимации (масштаб растет от 2 000 до 100 000 чисел)
frames_limits = np.linspace(2000, 100000, num=50, dtype=int)

# Создаем пустой графический объект (наша будущая фрактальная пыль)
scatter = ax.scatter([], [], color='magenta', s=1.5, alpha=0.7, edgecolors='none')

# Очищаем сетку полярных координат для космического эффекта
ax.set_rticks([])
ax.set_thetagrids([])
ax.spines['polar'].set_visible(False)

def init():
    """Начальное состояние кадра"""
    scatter.set_offsets(np.empty((0, 2)))
    return scatter,

def update(frame_idx):
    """Функция отрисовки каждого нового кадра"""
    current_limit = frames_limits[frame_idx]
    
    # Считаем данные для текущего масштаба
    twins = generate_primes_up_to(current_limit)
    D_current = calculate_d_fast(twins, current_limit)
    
    if len(twins) > 0:
        # Логарифмический радиус для красивого эффекта расширения вселенной
        theta = twins
        r = np.log(twins)
        
        # Переводим полярные координаты (углы и радиусы) в смещения для scatter-плота
        offsets = np.c_[theta, r]
        scatter.set_offsets(offsets)
        
        # Динамически раздвигаем границы графика вслед за ростом радиуса
        ax.set_rmax(np.log(current_limit) + 0.5)
    
    # Обновляем динамический заголовок-счетчик
    title_text = (
        f"DYNAMIC SIMULATOR: Twin Primes Evolution\n"
        f"Current Scale: 1 to {current_limit:,}\n"
        f"Live Hausdorff Dimension D = {D_current:.4f}"
    )
    ax.set_title(title_text, fontsize=12, color='lime', fontweight='bold', pad=30)
    return scatter,

# Запуск движка анимации (интервал 150 миллисекунд между кадрами)
ani = animation.FuncAnimation(
    fig, update, frames=len(frames_limits),
    init_func=init, blit=False, interval=150, repeat=False
)

print("[ИНФО] Интерактивный симулятор запущен! Наслаждайтесь эволюцией чисел...")
plt.show()
