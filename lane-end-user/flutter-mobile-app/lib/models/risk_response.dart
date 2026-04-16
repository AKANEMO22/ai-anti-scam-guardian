class RiskResponse {
  final int riskScore;
  final String explanation;
  final bool cacheHit;
  final List<MatchedPattern> matchedPatterns;

  RiskResponse({
    required this.riskScore,
    required this.explanation,
    this.cacheHit = false,
    this.matchedPatterns = const [],
  });

  factory RiskResponse.fromJson(Map<String, dynamic> json) {
    return RiskResponse(
      riskScore: json['riskScore'] ?? 0,
      explanation: json['explanation'] ?? '',
      cacheHit: json['cacheHit'] ?? false,
      matchedPatterns: (json['matchedPatterns'] as List? ?? [])
          .map((i) => MatchedPattern.fromJson(i))
          .toList(),
    );
  }
}

class MatchedPattern {
  final String patternId;
  final String patternText;
  final double score;

  MatchedPattern({
    required this.patternId,
    required this.patternText,
    required this.score,
  });

  factory MatchedPattern.fromJson(Map<String, dynamic> json) {
    return MatchedPattern(
      patternId: json['pattern_id'] ?? '',
      patternText: json['pattern_text'] ?? '',
      score: (json['score'] ?? 0.0).toDouble(),
    );
  }
}

enum SourceType {
  SMS,
  CALL,
  WEB,
}
