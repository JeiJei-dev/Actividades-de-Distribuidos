import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";
import { extractServicePort } from "./utils/extract-service-port.util";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.setGlobalPrefix("api");
  const port = await extractServicePort("logger-port");
  await app
    .listen(port)
    .then(() => console.log(`Logger listening on port ${port}`));
}
bootstrap();
