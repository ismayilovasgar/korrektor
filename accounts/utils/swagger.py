from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_override_serializer(self, serializer):
        # RegisterSerializer'a özel ref_name tanımlayın
        if serializer.__class__.__name__ == "RegisterSerializer":
            serializer.Meta.ref_name = "DjRestAuthRegisterSerializer"
        return super().get_override_serializer(serializer)
