// Variables
const carrito = document.querySelector("#carrito");
const listaProductos = document.querySelector("#lista-productos");
const contenedorCarrito = document.querySelector("#lista-carrito tbody");
const vaciarCarritoBtn = document.querySelector("#vaciar-carrito");
let productosCarrito = [];

// Listeners
cargarEventListeners();

function cargarEventListeners() {
  // Dispara cuando se presiona "Agregar al Carrito"
  if (listaProductos) {
    listaProductos.addEventListener("click", agregarProducto);
  }

  // Dispara cuando se presiona "Agregar al Carrito" en la cabecera
  const agregarCarritoHeader = document.querySelector(
    "#agregar-carrito-header"
  );
  if (agregarCarritoHeader) {
    agregarCarritoHeader.addEventListener(
      "click",
      agregarProductoDesdeCabecera
    );
  }

  // Cuando se elimina un producto del carrito
  carrito.addEventListener("click", eliminarProducto);

  // Al Vaciar el carrito
  if (vaciarCarritoBtn) {
    vaciarCarritoBtn.addEventListener("click", vaciarCarrito);
  }

  // Contenido cargado
  document.addEventListener("DOMContentLoaded", () => {
    productosCarrito =
      JSON.parse(localStorage.getItem("carrito")) || [];
    carritoHTML();
  });
}

// Función que añade el producto al carrito
function agregarProducto(e) {
  e.preventDefault();
  // Delegation para agregar-carrito
  if (e.target.classList.contains("agregar-carrito")) {
    const producto = e.target.parentElement.parentElement;
    // Enviamos el producto seleccionado para tomar sus datos
    leerDatosProducto(producto);
  }
}

// Lee los datos del producto
function leerDatosProducto(producto) {
  const infoProducto = {
    imagen: producto.querySelector("img").src,
    titulo: producto.querySelector("h4").textContent,
    precio: producto.querySelector(".precio span").textContent,
    id: producto.querySelector("a").getAttribute("data-id"), // Modificado aquí
    cantidad: 1,
 }


  if (productosCarrito.some((prod) => prod.id === infoProducto.id)) {
    const productos = productosCarrito.map((prod) => {
      if (prod.id === infoProducto.id) {
        let cantidad = parseInt(prod.cantidad);
        cantidad++;
        prod.cantidad = cantidad;
        return prod;
      } else {
        return prod;
      }
    });
    productosCarrito = [...productos];
  } else {
    productosCarrito = [...productosCarrito, infoProducto];
  }

  console.log(productosCarrito);

  carritoHTML();
}

// Elimina el producto del carrito en el DOM
function eliminarProducto(e) {
  e.preventDefault();
  if (e.target.classList.contains("borrar-producto")) {
    const producto = e.target.parentElement.parentElement;
    const productoId = producto.querySelector("a").getAttribute("data-id");

    // Eliminar del arreglo del carrito
    productosCarrito = productosCarrito.filter(
      (prod) => prod.id !== productoId
    );

    carritoHTML();
  }
}

// Muestra el producto seleccionado en el Carrito
function carritoHTML() {
  vaciarCarrito();

  productosCarrito.forEach((prod) => {
    const row = document.createElement("tr");
    row.innerHTML = `
               <td>  
                    <img src="${prod.imagen}" width=100>
               </td>
               <td>${prod.titulo}</td>
               <td>${prod.precio}</td>
               <td>${prod.cantidad} </td>
               <td>
                    <a href="#" class="borrar-producto" data-id="${prod.id}">X</a>
               </td>
          `;
    contenedorCarrito.appendChild(row);
  });

  // Sincronizar con el almacenamiento local
  sincronizarStorage();
}

// Sincronizar con el almacenamiento local
function sincronizarStorage() {
  localStorage.setItem("carrito", JSON.stringify(productosCarrito));
}

// Elimina los productos del carrito en el DOM
function vaciarCarrito() {
  // Forma rápida (recomendada)
  while (contenedorCarrito.firstChild) {
    contenedorCarrito.removeChild(contenedorCarrito.firstChild);
  }
}

console.log('Hola desde app.js');
