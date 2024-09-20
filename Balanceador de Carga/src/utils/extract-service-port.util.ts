export function extractServicePort(serviceName: string): number {
  return parseInt(
    process.argv
      .find((item: string) => item.includes(serviceName))
      .split("=")[1]
  );
}
