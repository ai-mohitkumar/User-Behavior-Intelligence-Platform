# ML Data Analytics Auto-Run TODO
Current Working Directory: c:/Users/mohit kumar/OneDrive/Desktop/optimization project

## Plan Summary
- Fix Streamlit LDA ValueError (n_components > n_classes-1)
- Add/enhance one-click 'Run ML Analysis' using sample CSV, auto graphs
- Fix backend imports for React UserBehaviorApp stability
- Ensure live graphs on browser (React + backend plots data)

## Steps
- [x] 1. Fix streamlit_intelligent_dashboard.py LDA error + add auto-run button with sample data (complete: LDA, scope, button)
- [x] 2. Fix UserBehaviorApp/backend/main.py imports (non-relative import + path)
- [x] Extra: Added auto-segment generation for LDA (no 'user_segment' warning gone, uses feature bins Low/Medium/High)
- [ ] 3. Add /auto-analyze endpoint in backend
- [ ] 4. Restart services, test localhost:3000/8501 auto analytics
- [ ] 5. Complete

