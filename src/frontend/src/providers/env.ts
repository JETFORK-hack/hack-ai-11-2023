function isIpAddressAndNotDomain(input: string): boolean {
  // Регулярное выражение для проверки IP-адреса
  const ipAddressPattern = /^(\d{1,3}\.){3}\d{1,3}$/;
  const cleanedUrl = input.replace(/^https?:\/\//, '');

  // Проверяем, соответствует ли входная строка IP-адресу
  return ipAddressPattern.test(cleanedUrl);
}

const readApiBaseFromEnv = (): string => {
  // Get API base URL from env
  // Priority is given to same host in the browser when environemnt is production
  if (
    import.meta.env.PROD &&
    !document.location.host.startsWith("localhost")
  ) {
    return `https://${document.location.host}`;
  } else if (import.meta.env.BASE_URL && import.meta.env.BASE_URL !== "/") {
    return import.meta.env.BASE_URL;
  }
  return "http://localhost:8000";
};

export const basePath: string = readApiBaseFromEnv();
