import { NestFactory } from "@nestjs/core";
import { ValidationPipe } from "@nestjs/common";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Global prefix for all API endpoints
  app.setGlobalPrefix("api/v1");

  // Global validation pipe
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      transform: true,
      forbidNonWhitelisted: true,
    }),
  );

  // Enable CORS
  const corsOrigins = process.env.CORS_ALLOWED_ORIGINS
    ? process.env.CORS_ALLOWED_ORIGINS.split(",")
    : ["http://localhost:5173"];

  app.enableCors({
    origin: corsOrigins,
    credentials: true,
  });

  const port = process.env.SERVER_PORT || 8080;
  await app.listen(port);
  console.log(`EduBranch AI Backend Gateway listening on port ${port} (prefix: /api/v1)`);
}

bootstrap();
