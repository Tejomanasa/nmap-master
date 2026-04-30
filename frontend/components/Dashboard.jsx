import { Award, BarChart3, Trophy } from "lucide-react";

export function Dashboard({ progress, modules }) {
  const completed = progress?.completed_modules?.length || 0;
  const percent = Math.round((completed / modules.length) * 100);

  return (
    <section className="dashboard-band">
      <div className="stat">
        <BarChart3 size={21} />
        <span>Progress</span>
        <strong>{percent}%</strong>
      </div>
      <div className="stat">
        <Trophy size={21} />
        <span>XP</span>
        <strong>{progress?.xp || 0}</strong>
      </div>
      <div className="stat">
        <Award size={21} />
        <span>Level</span>
        <strong>{progress?.level || 1}</strong>
      </div>
      <div className="badges">
        {(progress?.badges || ["No badges yet"]).slice(0, 6).map((badge) => (
          <span key={badge}>{badge}</span>
        ))}
      </div>
    </section>
  );
}
