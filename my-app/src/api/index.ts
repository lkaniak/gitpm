import axios, { AxiosRequestConfig } from "axios";
import { isDevelopment } from "~/shared/globals";

const instance = axios.create({
	baseURL: process.env.APP_BACKEND_URL,
});

export enum HttpMethods {
  GET = "GET",
  POST = "POST",
  PATCH = "PATCH",
  DELETE = "DELETE",
  PUT = "PUT",
  OPTIONS = "OPTIONS"
}

interface Parameter {
  [propName: string]: string | number
}

interface WrapperProps {
  url: string,
  config?: AxiosRequestConfig<any>
}

interface GetProps extends WrapperProps {
}

interface DeleteProps extends WrapperProps {
}

interface PostProps extends WrapperProps {
  body: any,
}

interface PatchProps extends WrapperProps {
  body: any,
}

interface PutProps extends WrapperProps {
  body: any,
}

interface OptionsProps extends WrapperProps {}

const wrapper = {
  [HttpMethods.GET]: async (props:GetProps) => {
    return await instance.get(props.url, props.config);
  },
  [HttpMethods.POST]: async (props:PostProps) => {
    return await instance.post(props.url, props.config);
  },
  [HttpMethods.PATCH]: async (props:PatchProps) => {
    return await instance.patch(props.url, props.config);
  },
  [HttpMethods.DELETE]: async (props:DeleteProps) => {
    return await instance.delete(props.url, props.config);
  },
  [HttpMethods.PUT]: async (props:PutProps) => {
    return await instance.put(props.url, props.config);
  },
  [HttpMethods.OPTIONS]: async (props:OptionsProps) => {
    return await instance.options(props.url, props.config);
  },
}

interface ApiCallProps {
  method: HttpMethods,
  url: string,
  params?: Parameter
  data?: any,
}

async function api(props: ApiCallProps) {
  let qs = ""
  let url = props.url;
  const params = Object.keys(props.params ?? {});
  params.forEach(p => qs += `${p}=${props.params[p]}`);
  if (qs) {
    qs = "?" + qs
    url += qs
  }
  try {
    const res = await wrapper[props.method]({ url, body: props.data });
    return res.data;
  } catch (error) {
    // if (isDevelopment) {
    //   console.error(error.config);
    // }
    if (error.response) {
      if (isDevelopment) {
        console.error(error.response.data);
      }
      if (error.response.data?.status_message) {
        return error.response.data.status_message;
      }

      if ([500, 422].includes(error.response.status)) {
        return "Erro ao processar a requisição."
      }

    } else if (error.request) {
      if (isDevelopment) {
        console.error(error.request);
      }
      return "Erro ao solicitar a requisição."
    } else {
      if (isDevelopment) {
        console.error(error.message);
      }
    }
  }
}

export default api;


