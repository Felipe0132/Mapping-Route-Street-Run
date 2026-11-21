import gpxpy
import networkx as nx


class GPXFormatError(ValueError):
    """Exceção lançada quando o arquivo .GPX não segue a estrutura padrão esperada."""
    pass


def extract_points_gpx(file_gpx):
    # Extract point to point in gpx file
    try:
        if hasattr(file_gpx, 'seek'):
            file_gpx.seek(0)

        if isinstance(file_gpx, str):  # If receive string in st.upload
            with open(file_gpx, 'r', encoding='utf-8') as f:
                gpx = gpxpy.parse(f)
        else:
            gpx = gpxpy.parse(file_gpx)
    except Exception as exc:
        raise GPXFormatError(
            "O arquivo enviado não pôde ser lido como um GPX válido. "
            "Utilize o padrão GPX com a mesma estrutura do trajeto de exemplo (Corrida Viveza)."
        ) from exc

    if not getattr(gpx, 'tracks', None):
        raise GPXFormatError(
            "O arquivo .GPX não possui trilhas (<trk> / <trkseg> / <trkpt>). "
            "Utilize o padrão GPX com a mesma estrutura do trajeto de exemplo (Corrida Viveza)."
        )

    points = []
    points_aux = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if point.latitude is None or point.longitude is None or point.elevation is None:
                    raise GPXFormatError(
                        "O arquivo .GPX possui pontos sem coordenadas (lat/lon) ou sem altitude (<ele>). "
                        "Utilize o padrão GPX com a mesma estrutura do trajeto de exemplo (Corrida Viveza)."
                    )
                ponto_aux = {
                    'lng': point.longitude,
                    'lat': point.latitude,
                    'elev': point.elevation
                }
                if not points or ponto_aux != points[-1]:
                    points.append(ponto_aux)
                    points_aux.append(ponto_aux)

    if len(points) < 2:
        raise GPXFormatError(
            "O arquivo .GPX não contém pontos suficientes para montar o percurso. "
            "Utilize o padrão GPX com a mesma estrutura do trajeto de exemplo (Corrida Viveza)."
        )

    return points
