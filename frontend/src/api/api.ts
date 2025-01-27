import axios from "axios";


const api = axios.create({
  baseURL: "http://localhost:8000/api",
})

interface ProductInterface {
  name: string,
  description: string,
  price: number,
  image: File | null
}


export const getProducts = async () => {
  return await api.get('/products/')
}

export const getProduct = async (id: number) => {
  return await api.get(`/products/${id}/`)
}

export const createProduct = async (data: ProductInterface) => {
  return await api.post('/products/', data,{
    headers:{
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const updateProduct = async (id: number, data: ProductInterface) => {
  return await api.put(`/products/${id}/`, data,{
    headers:{
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const deleteProduct = async (id: number) => {
  return await api.delete(`/products/${id}/`)
}