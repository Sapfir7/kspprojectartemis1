import math

# Глобальные константы KSP для Кербина (Земля)
G = 6.6741 * 10**-11  # [Н*м^2 / кг^2]
Rk = 600000  # [м] - радиус Кербина
Mk = 5.2916 * 10**22  # [кг]
g0 = 9.81  # [м / с^2]
mu = 3.5316 * 10**12  # G*M - гравитационный параметр, [м^3 / c^2]

# Остальные параметры
p0 = 101325  # [Па]
R = 8.31  # [Дж / (моль∙К)]
T = 273  # [К]
M = 0.029  # [кг / моль]
Kf = (p0 * M) / (R * T)

# Параметры ракеты
S = 40  # [м^2] подобрать, нввв
Cf = 0.65
b = 2900
Mr = 760000

# Параметры для рассчета угла отклонения от нормали
start_h = 100  # [м]
end_h = 45000  # [м]  - радиус закругления
start_v = 100
end_v = 1300


def Thrust(M):
    if M > 467000:
        return 13600000
    else:
        return 8160000


def cosn(v):
    if v > start_v and v < end_v:
        frac = (v - start_v) / (end_v - start_v)
        beta = frac * (math.pi / 2)

        return math.cos(beta)
    elif v < start_v:
        return 1

    if v >= end_v:
        beta = (89.7 / 90) * (math.pi / 2)

        return math.cos(beta)


def sinn(v):
    if v > start_v and v < end_v:
        frac = (v - start_v) / (end_v - start_v)
        beta = frac * (math.pi / 2)

        return math.sin(beta)
    elif v < start_v:
        return 0

    if v >= end_v:
        beta = (89.7 / 90) * (math.pi / 2)

        return math.sin(beta)



def cosnh(h):
    if h > start_h and h < end_h:
        frac = (h - start_h) / (end_h - start_h)
        beta = frac * (math.pi / 2)

        return math.cos(beta)
    elif h < start_h:
        return 1

    if h >= end_h:
        beta = (89.7 / 90) * (math.pi / 2)

        return math.cos(beta)


def sinnh(h):
    if h > start_h and h < end_h:
        frac = (h - start_h) / (end_h - start_h)
        beta = frac * (math.pi / 2)

        return math.sin(beta)
    elif h < start_h:
        return 0

    if h >= end_h:
        beta = (89.7 / 90) * (math.pi / 2)

        return math.sin(beta)


def flight(log_file):
    t = 0
    dt = 1
    h = 20
    vr = 0
    vt = 0
    v = 0
    beta = 0
    current_mass = Mr
    log_file.write(
        "Time"
        + ": "
        + "Velocity\tHeight\tAngle\tMass\tRad. velocity\tTan. velocity\n"
        + f"{t:.4f}: {v:.8f} - {h:.8f} - {beta:.8f} - {current_mass:.8f} - {vr:.8f} - {vt:.8f}"
        + "\n"
    )
    while t <= 169:
        current_mass = Mr - b * t
        g = (G * Mk) / ((Rk + h) ** 2)
        ar = (
            Thrust(current_mass) * cosn(h)
            - (current_mass) * g
            - (
                (Cf * S * (Kf * math.exp(-((M * g * h) / (R * T)))))
                * (v**2)
                * cosn(h)
            )
            / 2
        ) / (current_mass)

        at = (
            Thrust(current_mass) * sinn(h)
            - (
                (Cf * S * (Kf * math.exp(-((M * g * h) / (R * T)))))
                * (v**2)
                * sinn(h)
            )
            / 2
        ) / current_mass
        vr = vr +  ar * dt
        vt = vt + at * dt
        v = (vt**2 + vr**2) ** 0.5
        h = h +  vr * dt
        t += dt
        beta = math.acos(cosn(h)) / (math.pi / 2) * 90

        log_file.write(
            f"{t:.4f}: {v:.8f} - {h:.8f} - {beta:.8f} - {current_mass:.8f} - {vr:.8f} - {vt:.8f}"
            + "\n"
        )


def main():
    log_file = open("old_mat.txt", "w")
    flight(log_file)
    log_file.close()


main()


