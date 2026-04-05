use anchor_lang::prelude::*;

declare_id!("QaL1on5mBdZFvgFjSJGnmVZWe2FsBM3VN47L6PemxGWy");

// ─── Events ────────────────────────────────────────────────────────────────

#[event]
pub struct ReconstructionComplete {
    pub entity_id: String,
    pub domain: String,
    pub confidence: f64,
    pub temporal_depth_years: u32,
    pub risk_level: String,    // "LOW" | "MEDIUM" | "HIGH"
    pub result_hash: [u8; 32],
    pub timestamp: i64,
}

// ─── Accounts ──────────────────────────────────────────────────────────────

#[account]
pub struct QalReconRecord {
    pub authority: Pubkey,
    pub entity_id: String,          // max 64 bytes
    pub domain: String,             // max 32 bytes
    pub confidence: f64,            // 0.0–1.0
    pub temporal_depth_years: u32,
    pub risk_level: String,         // max 8 bytes
    pub result_hash: [u8; 32],
    pub timestamp: i64,
    pub bump: u8,
}

impl QalReconRecord {
    pub const LEN: usize = 8 + 32 + (4 + 64) + (4 + 32) + 8 + 4 + (4 + 8) + 32 + 8 + 1;
}

// ─── Error codes ───────────────────────────────────────────────────────────

#[error_code]
pub enum QalError {
    #[msg("Entity ID must not be empty")]
    EmptyEntityId,
    #[msg("Domain must not be empty")]
    EmptyDomain,
    #[msg("Confidence must be between 0.0 and 1.0")]
    InvalidConfidence,
    #[msg("Invalid risk level: must be LOW, MEDIUM, or HIGH")]
    InvalidRiskLevel,
    #[msg("Unauthorized: signer is not the record authority")]
    Unauthorized,
}

// ─── Program ───────────────────────────────────────────────────────────────

#[program]
pub mod qal {
    use super::*;

    /// Begin a QAL historical reconstruction for an entity.
    pub fn begin_reconstruction(
        ctx: Context<BeginReconstruction>,
        entity_id: String,
        domain: String,
        temporal_depth_years: u32,
    ) -> Result<()> {
        require!(!entity_id.is_empty(), QalError::EmptyEntityId);
        require!(!domain.is_empty(), QalError::EmptyDomain);

        let record = &mut ctx.accounts.recon_record;
        let clock = Clock::get()?;

        record.authority = ctx.accounts.authority.key();
        record.entity_id = entity_id;
        record.domain = domain;
        record.confidence = 0.0;
        record.temporal_depth_years = temporal_depth_years;
        record.risk_level = "MEDIUM".to_string();
        record.result_hash = [0u8; 32];
        record.timestamp = clock.unix_timestamp;
        record.bump = ctx.bumps.recon_record;

        Ok(())
    }

    /// Complete a QAL reconstruction, recording results and emitting event.
    pub fn complete_reconstruction(
        ctx: Context<CompleteReconstruction>,
        confidence: f64,
        risk_level: String,
        result_hash: [u8; 32],
    ) -> Result<()> {
        require!(confidence >= 0.0 && confidence <= 1.0, QalError::InvalidConfidence);
        require!(
            matches!(risk_level.as_str(), "LOW" | "MEDIUM" | "HIGH"),
            QalError::InvalidRiskLevel
        );

        let record = &mut ctx.accounts.recon_record;
        require!(record.authority == ctx.accounts.authority.key(), QalError::Unauthorized);

        let clock = Clock::get()?;
        let entity_id = record.entity_id.clone();
        let domain = record.domain.clone();
        let temporal_depth_years = record.temporal_depth_years;

        record.confidence = confidence;
        record.risk_level = risk_level.clone();
        record.result_hash = result_hash;
        record.timestamp = clock.unix_timestamp;

        emit!(ReconstructionComplete {
            entity_id,
            domain,
            confidence,
            temporal_depth_years,
            risk_level,
            result_hash,
            timestamp: clock.unix_timestamp,
        });

        Ok(())
    }
}

// ─── Instruction Contexts ──────────────────────────────────────────────────

#[derive(Accounts)]
#[instruction(entity_id: String)]
pub struct BeginReconstruction<'info> {
    #[account(
        init,
        payer = authority,
        space = QalReconRecord::LEN,
        seeds = [b"recon", entity_id.as_bytes()],
        bump,
    )]
    pub recon_record: Account<'info, QalReconRecord>,

    #[account(mut)]
    pub authority: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct CompleteReconstruction<'info> {
    #[account(
        mut,
        seeds = [b"recon", recon_record.entity_id.as_bytes()],
        bump = recon_record.bump,
    )]
    pub recon_record: Account<'info, QalReconRecord>,

    pub authority: Signer<'info>,
}
