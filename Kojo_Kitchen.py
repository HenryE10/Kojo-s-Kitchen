import Generation_Var
import random
import sys
from math import sqrt

def Generating_Client(t,_lambda):
    type_food = random.randint(0,1)#0 sandwiches , 1 suchis

    client = (type_food ,t + Generation_Var.Exponential_Var(_lambda))
    return client

def Generating_Time_Suchi(t):
    return t + Generation_Var.UniformAB_Var(5,8)*60


def Generating_Time_Sandwish(t):
    return t + Generation_Var.UniformAB_Var(3,5)*60


def Kojo_Kitchen(extra_worker=False, normal_lambda=1/600, rush_hour_lambda=1/150):
                       
    opened = True  #Estado de la tienda(True-Abierta),(Close-Cerrada)
    t = 0 # tiempo de la simulación
    T = 11 * 60 * 60 # tiempo en que cierra la tienda en segundos
    rush_hour1 = (90*60, 210*60) # primera hora pico de 11:30 a 1:30
    rush_hour2 = (7*60*60, 9*60*60)# segunda hora pico de 5:00 a 7:00
    clients = 0

    inf = sys.maxsize
    state_worker = [False, False] # Estado de los trabajadores si están ocupados con un cliente o libres
    worker_clients = [0, 0, 0]  #cantidad de clientes q ha atendido el trabajador i
    all_td = [inf, inf, inf] #tiempo de salida de el cliente atendido por el trabajor i

    queue_clients = []
    te = [] #tiempo de espera de cada cliente en la cola

    client = Generating_Client(t, normal_lambda)
    ta = client[1] #tiempo del próximo arribo
    

    sale_type = [0,0] #Cuantos sandwiches se vendieron y cuantos suchi

    e = 0 #los que esperan mas de 5 minutos en ser atendidos



    while opened or any(state_worker):
        td = min(all_td)

        if(ta < td and ta < T):#Turno de llegada de un cliente en hora de trabajo
            t = ta
            clients += 1

            queue_clients.append(client)
            #Al dezplazar el tiempo callo en la hora pico tengo que agregar al nuevo dependiente en caso de estar probando un trabajador extra
            if((rush_hour1[0]<= t <= rush_hour1[1]) or (rush_hour2[0]<= t <= rush_hour2[1])):
                if(extra_worker and len(state_worker) == 2):
                    state_worker.append(False)

            else:
                 if(len(state_worker) == 3 and not state_worker[2]):
                    state_worker.pop()


            if(not all(state_worker)):
                for i in range(len(state_worker)):
                    if(state_worker[i] == False):
                        worker = i
                        break
                
                c = queue_clients.pop()
                te.append(t - c[1])
                if(t - c[1] > 5*60):
                    e+=1


                state_worker[worker] = True
                worker_clients[worker] += 1
                sale_type[c[0]] += 1

                
                if (c[0] == 0):
                    all_td[worker] = Generating_Time_Sandwish(t)
                else:
                    all_td[worker] = Generating_Time_Suchi(t)


            if((rush_hour1[0]<= t <= rush_hour1[1]) or (rush_hour2[0]<= t <= rush_hour2[1])):
                client = Generating_Client(t,rush_hour_lambda)
                ta = client[1]
                


            else:
                client = Generating_Client(t,normal_lambda)
                ta = client[1]
               


        elif(td < ta or (any(state_worker) and not opened)):
            
            for i in range(len(all_td)):
                if(all_td[i] == td):
                    client_out = i

            t = td
            
            #Al dezplazar el tiempo callo en la hora pico tengo que agregar al nuevo dependiente en caso de estar probando un trabajador extra 
            # si hay clientes en cola pasarle uno
            if((rush_hour1[0]<= t <= rush_hour1[1]) or (rush_hour2[0]<= t <= rush_hour2[1])):
                if(extra_worker and len(state_worker) == 2):
                    state_worker.append(False)

                    if(len(queue_clients) > 0):
                        ca = queue_clients.pop()
                        te.append(t - ca[1])
                        if(t - c[1] > 5*60):
                            e+=1

                        if (ca[0] == 0):
                            all_td[2] = Generating_Time_Sandwish(t)
                        else:
                            all_td[2] = Generating_Time_Suchi(t)
                    
                        state_worker[2] = True
                        worker_clients[2] += 1
                        sale_type[ca[0]] += 1
      
                else:
                    if(len(state_worker) == 3 and not state_worker[2]):
                        state_worker.pop()

            if(len(queue_clients) > 0):
                c = queue_clients.pop()
                te.append(t - c[1])
                if(t - c[1] > 5*60):
                    e+=1

                if (c[0] == 0):
                    all_td[client_out] = Generating_Time_Sandwish(t)
                else:
                    all_td[client_out] = Generating_Time_Suchi(t)
                
                state_worker[client_out] = True
                worker_clients[client_out] += 1
                sale_type[c[0]] += 1

            else:
                state_worker[client_out] = False
                all_td[client_out] = inf

        if(ta > T):
            ta = inf 
            opened = False

        if(t > T):
            opened = False


    ret = e/len(te) * 100
    return te, worker_clients, sale_type, ret, e


def main():
    cant_personas_diaria = 0
    empleado1 = 0
    empleado2 = 0
    suchi = 0
    sandwiches = 0
    et = 0
    ret_total = 0
    
    print('Resultados de simular 25 dias de trabajo con 2 empleados')

    for _ in range(25):
        te1, worker_clients1, sale_type1, ret1, e1 = Kojo_Kitchen()
        cant_personas_diaria += len(te1)
        empleado1 += worker_clients1[0]
        empleado2 += worker_clients1[1]
        suchi += sale_type1[1]
        sandwiches += sale_type1[0]
        et += e1
        ret_total += ret1
    

    print(f'El promedio de clientes que arribaron diariamente en la primera simulacion es: {cant_personas_diaria/25} ')
    print(f'El promedio de personas diarias atendidas por el empleado1 es: {empleado1/25} y por el empleado2 es: {empleado2/25}')
    print(f'El promedio de platos diarios de suchi e:s {suchi/25} y de sandwiches es: {sandwiches/25}')
    print(f'El promedio de clientes diarios que espera más de 5 minutos en cola para ser atendidos es: {et/25}')
    print(f'La media diaria del porciento de clientes con tiempo de espera mayor que 5 minutos en cola para dos dependientes: {ret_total/25}' )



    print('Resultados de simular 25 dias de trabajo con 2 empleados y una adicional en horas pico')
    cant_personas_diaria = 0
    empleado1 = 0
    empleado2 = 0
    empleado3 = 0
    suchi = 0
    sandwiches = 0
    et = 0
    ret_total = 0
    for _ in range(25):
        te2, worker_clients2, sale_type2, ret2, e2 = Kojo_Kitchen(True)
        cant_personas_diaria += len(te2)
        empleado1 += worker_clients2[0]
        empleado2 += worker_clients2[1]
        empleado3 += worker_clients2[2]
        suchi += sale_type2[1]
        sandwiches += sale_type2[0]
        et += e2
        ret_total += ret2
    
    print(f'El promedio de clientes que arribaron diariamente en la segunda simulacion es: {cant_personas_diaria/25} ')
    print(f'El promedio de personas diarias atendidas por el empleado1 es: {empleado1/25}, por el empleado2 es {empleado2/25} y por el empleado3 es: {empleado3/25}')
    print(f'El promedio de platos diarios de suchi es {suchi/25} y de sandwiches es {sandwiches/25}')
    print(f'El promedio de clientes diarios que espera más de 5 minutos en cola para ser atendidos es: {et/25}')
    print(f'La media diaria del porciento de clientes con tiempo de espera mayor que 5 minutos en cola para dos dependientes y uno extra en horas picos es: {ret_total/25}' )

    print('Finish')
main()
