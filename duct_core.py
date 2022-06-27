# Copyright @alexelaxing 2022
# Calculate method as per 2013 ASHRAE Handbook - Fundamentals(SI), Chapter 21
import math

def sizing(vdot, roughness):
    # Initiate
    from decimal import Decimal, getcontext, Context
    getcontext().prec = 2

    # List all variable

    flowrate = 250  ###Volumetric flow rate, l/s
    deltaPf = 1.0  # friction losses in terms of total pressure, Pa
    f = 1.0  # friction factor, dimensionless, to nearest 0.001
    f_temp = 1.0  # estimated friction factor, dimensionless
    L = 1.0  # duct length, m
    Dh = 1.0  # hydraulic diameter, mm
    velocity = 1.0  # velocity, m/s
    rho = 1.204  # density, kg/m^3 (20 °C and 101.325 kPa)
    epsilon = 1  ###material absolute roughness factor, mm
    Re = 1.0  # Reynolds number
    area = 1.0  # duct area, mm2
    perimeter = 1.0  # perimeter of cross section, mm
    De = 1.0  # circular equivalent of rectangular duct for equal length, fluid resistance, and airflow, mm
    a = 4000.0  ###length one side of duct, mm
    b = 14000.0  ###length adjacent side of duct, mm

    # input
    #a = side1  ###length one side of duct, mm
    #b = side2  ###length adjacent side of duct, mm
    flowrate = vdot
    epsilon = roughness

    # Calculation
    flowrate = flowrate / 1000  # Convert to m3/s
    a = flowrate / 8 # flowrate / 8m/s to get area
    a = math.sqrt(a) * 1000
    b=a

    De=1.3*(a*b)**0.625/(a+b)**0.25						#(25), calculate equiv. diameter
    velocity = flowrate / (math.pi * ((De / 2000) ** 2))  # Calculate the airflow velocity
    area = (a * b)
    perimeter = (a + a + b + b)
    Dh = 4 * area / perimeter  # (24)
    Re = 66.4 * Dh * velocity  # (21)
    f = (1 / (-1.8 * math.log10(
        ((6.9 / Re) + ((epsilon / Dh) / 3.71) ** 1.11)))) ** 2  # Estiamtion using CIBSE method (Haaland)
    f_temp = f  # Compare Haaland estimation with Colebrook's



    velocity = flowrate / (math.pi * ((De / 2000) ** 2))  # Calculate the airflow velocity
    deltaPf = ((1000 * f * L) / Dh) * ((rho * (velocity ** 2)) / 2)  # (18)



    # Colebrook’s equation
    RHS = -2 * math.log10((epsilon / (3.7 * Dh)) + (2.51 / (Re * math.sqrt(f))))
    LHS = 1 / math.sqrt(f)

    print ("RHS=",RHS, "LHS=", LHS)
    if RHS != LHS:
        temp = RHS - LHS
        print(temp)
        print(f)
        # print ("temp the first time: ",temp)
        while temp > 0.001:
            f = f - 0.00001
            RHS = -2 * math.log10((epsilon / (3.7 * Dh)) + (2.51 / (Re * math.sqrt(f))))
            LHS = 1 / math.sqrt(f)
            temp = RHS - LHS
            print("f end=", f)
            print("temp end=", temp)
        # print ("Condition 1", temp)
        while temp < -0.001:
            f = f + 0.00001
            RHS = -2 * math.log10((epsilon / (3.7 * Dh)) + (2.51 / (Re * math.sqrt(f))))
            LHS = 1 / math.sqrt(f)
            temp = RHS - LHS
            print("f end=", f)
            print("temp end=", temp)
        # print ("Condition 2", temp)

    deltaPf = ((1000 * f * L) / Dh) * ((rho * (velocity ** 2)) / 2)  # (18)

    # output
    print("The flowrate is: ", round(flowrate, 3), "m³/s")
    print("The velocity is: ", round(velocity, 2), "m/s")
    print("The equiv. diameter is: ", round(De, 2), "mm")
    print("The Area is: ", round(area / 1000000, 2), "m²")
    print("The perimeter is: ", round(perimeter, 2), "mm")
    print("The hydralic diameter is: ", round(Dh, 2), "mm")
    print("The Reynolds number is:", round(Re, 2))
    print("The estimated friction factor is:", round(f_temp, 5))
    print("The friction factor is:", round(f, 5))
    print("The percentage different is: ", round((f - f_temp) * 100 / f, 3), "%")
    print("The friction loss is: ", round(deltaPf, 2), "Pa/m")

    return flowrate, area, velocity, deltaPf

if __name__ == '__main__':
    sizing (50,0.15)