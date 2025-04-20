def vender_acciones(compras, cantidad_a_vender, precio_venta):
    """Vendemos las acciones mas viejas primero (FIFO) y calculamos la ganancia total."""
    ganancia_total = 0
    cantidad_restante = cantidad_a_vender

    while cantidad_restante > 0 and compras:
        compra = compras[0]
        if compra['cantidad'] <= cantidad_restante:
            # Vender toda la compra
            cantidad_vendida = compra['cantidad']
            ganancia = cantidad_vendida * (precio_venta - compra['precio_unitario'])
            ganancia_total += ganancia
            cantidad_restante -= cantidad_vendida
            compras.pop(0)
        else:
            # Vender parcialmente
            cantidad_vendida = cantidad_restante
            ganancia = cantidad_vendida * (precio_venta - compra['precio_unitario'])
            ganancia_total += ganancia
            compra['cantidad'] -= cantidad_vendida
            cantidad_restante = 0

    if cantidad_restante > 0:
        print("⚠️ No hay suficientes acciones para vender.")

    return ganancia_total, compras