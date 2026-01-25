# Denne løsningen bygger på
# https://math.libretexts.org/Courses/Cosumnes_River_College/Math_420%3A_Differential_Equations_(Breitenbach)/06%3A_Applications_of_Linear_Second_Order_Equations/6.02%3A_Spring-Mass_Problems_(With_Damping)

import numpy as np

def analytisk_svingning(M, alpha, k, t0, x0, y0):
    """
    Beregner den analytiske løsningen for en dampet harmonisk oscillator.

    Denne funksjonen løser en differensialligning som beskriver bevegelsen til et system
    bestående av en masse (M) festet til en fjær med konstant (k), hvor systemet er 
    dempet av en faktor (alpha). Avhengig av verdien av diskriminanten, vil løsningen være
    enten eksponentielt avtagende, oscillerende, eller kritisk dempet.

    Args:
        M (float): Massens verdi (kg).
        alpha (float): Dempingsfaktoren (kan være positiv).
        k (float): Fjærkonstanten (N/m).
        t0 (float): Starttidspunkt (s).
        x0 (float): Startposisjon (m).
        y0 (float): Starthastighet (m/s).

    Returns:
        tuple: To funksjoner (x, y) som beskriver posisjon og hastighet over tid.
            - x(t) (funksjon): Posisjonen til systemet som funksjon av tid t.
            - y(t) (funksjon): Hastigheten til systemet som funksjon av tid t.
    
    Løsningene er basert på verdien av diskriminanten D:
        - Hvis D > 0 (to reelle røtter): Løsningene for x(t) og y(t) er eksponentielt avtagende.
        - Hvis D < 0 (komplekse røtter): Løsningene for x(t) og y(t) inneholder en oscillasjon med demping.
        - Hvis D = 0 (kritisk demping): Løsningene for x(t) og y(t) er lineære med eksponentiell avtagning.
    """
    # Beregner p og q som er nødvendige for å løse den analytiske løsningen
    p = k / M  # p = k/M
    q = alpha / M  # q = alpha/M
    
    # Beregner diskriminanten D (D = q^2 - 4p), som avgjør type løsning
    D = q**2 - 4*p

    if D > 0:
        # Når D er positiv, finnes to forskjellige løsninger for eksponentiell vekst
        # Beregn røttene lambda1 og lambda2 ved hjelp av funksjonene ff og gg
        lambda1 = ff(1, q, p)  # Første rot (lambda1)
        lambda2 = gg(1, q, p)  # Andre rot (lambda2)
        
        # Beregn konstantene C1 og C2 basert på initialbetingelsene (x0, y0)
        C2 = (y0 - lambda1 * x0) / (lambda2 - lambda1)  # Beregn C2
        C1 = x0 - C2  # Beregn C1
        
        # Definerer funksjonen x(t) som beskriver bevegelsen over tid
        def x(t):
            s = t - t0  # Tidsskift (forsinkelse i tid)
            return C1 * np.exp(lambda1 * s) + C2 * np.exp(lambda2 * s)  # Løsning for x(t)
        
        # Definerer funksjonen y(t) som beskriver bevegelsen over tid for y
        def y(t):
            s = t - t0  # Tidsskift
            return C1 * np.exp(lambda1 * s) * lambda1 + C2 * np.exp(lambda2 * s) * lambda2  # Løsning for y(t)
    
    elif D < 0:
        # Når D er negativ, er løsningen en oscillering (komplekse røtter)
        omega = np.sqrt(-D) / 2  # Beregner den oscillerende frekvensen (omega)
        
        # Beregn konstantene C1 og C2 basert på initialbetingelsene (x0, y0)
        C2 = (y0 + (q * x0) / 2) / omega  # Beregn C2
        C1 = x0  # Sett C1 lik x0
        
        # Definerer funksjonen x(t) som beskriver bevegelsen over tid med oscillasjon
        def x(t):
            s = t - t0  # Tidsskift
            return np.exp(-q * s / 2) * (C1 * np.cos(omega * s) + C2 * np.sin(omega * s))  # Løsning for x(t)
        
        # Definerer funksjonen y(t) som beskriver bevegelsen over tid for y
        def y(t):
            s = t - t0  # Tidsskift
            return - 0.5 * q * x(t) + omega * np.exp(-q * s / 2) * (-C1 * np.sin(omega * s) + C2 * np.cos(omega * s))  # Løsning for y(t)
    
    else:
        # Når D er null, er løsningen kritisk demping (en rot)
        C1 = x0  # Sett C1 lik x0
        C2 = y0 + (2 * x0) / q  # Beregn C2
        
        # Definerer funksjonen x(t) som beskriver bevegelsen over tid med kritisk demping
        def x(t):
            s = t - t0  # Tidsskift
            return np.exp(-q * s / 2) * (C1 + C2 * s)  # Løsning for x(t)
        
        # Definerer funksjonen y(t) som beskriver bevegelsen over tid for y
        def y(t):
            s = t - t0  # Tidsskift
            return np.exp(-q * s / 2) * (-0.5 * q * (C1 + C2*s) + C2)  # Løsning for y(t)
    
    # Returnerer funksjonene x(t) og y(t) som kan brukes til å beregne bevegelsen over tid
    return x, y